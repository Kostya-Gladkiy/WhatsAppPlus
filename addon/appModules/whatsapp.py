import appModuleHandler
import api
import scriptHandler
from scriptHandler import script
from ui import message
import controlTypes
from keyboardHandler import KeyboardInputGesture
import addonHandler
import config
import speech
import time
from  threading import Timer
import winUser
import mouseHandler
import queueHandler
import languageHandler
import os
import sys
sys.path.insert(0, ".")
from .text_window import *
from nvwave import playWaveFile
from re import *

reg_for_delete_phon_number = compile(r"\+\d[()\d\s‬-]{12,}")

baseDir = os.path.join(os.path.dirname(__file__), "media\\")

addonHandler.initTranslation()

icon_from_context_menu = {
	"reply to message": "\ue97a",
	"edit message": "\ue70f",
	"react": "\ue76e",
	"forward message": "\uee35",
	"delete": "\ue74d",
	"mark as read": "\ue8bd",
	"mark as unread": "\ue668",
	"leave the group": "\ue89b",
	"star message": "\ue734",
	"remove from starred messages": "\ue735",
	"save as": "\ue74e",
	"select message": "\ue73a",
}

lang = languageHandler.getLanguage().split("_")[0]

phrases_of_unread_messages = {
	"uk": "непрочитані повідомлення,непрочитаних повідомлень, непрочитане повідомлення",
	"tr": "okunmamış mesaj",
	"es": "mensajes no leídos",
	"it": "messaggi non letti,messaggio non letto",
	"en": "unread messages,unread message",
	"ro": "mesaje necitite",
	"ru": "непрочитанное сообщение,непрочитанные сообщения,непрочитанных сообщения",
	"sr": "nepročitane poruke",
	"hr": "nepročitanih poruka,nepročitane poruke,nepročitana poruka",
}

SPEC = {
	'playSoundWhenRecordingVoiceMessage': 'boolean(default=False)',
	'phrasesOfUnreadMessages': 'string(default="'+phrases_of_unread_messages.get(lang, "en")+'")',
	'number_phone': 'string(default="")',
	'user_name': 'string(default="")',
	'isAutomaticallyCheckForUpdates': 'boolean(default=True)',
	'displayPhoneNumberInUsername': 'boolean(default=True)',
	'automaticReadingOfNewMessages': 'boolean(default=False)',
	'automatically_report_progress_indicators': 'boolean(default=False)',
	'automatically announce activity in chats': 'boolean(default=True)',
}


class Title_change_tracking:
	app = False
	active = False
	pouse = False
	interval = .5
	last_value = None
	@classmethod
	def tick(cls):
		if not cls.active or cls.pouse: return
		try:
			title = Chat_update.app.get_title_element()
			chat_name = title.children[2].name
			sub_title = title.children[3].name if len(title.children) == 4 else ""
		except Exception as e:
			title = None
		if not title or not title.isInForeground:
			cls.pouse = True
			return False
		last_value = cls.last_value or ("", "")
		if sub_title != last_value[1]:
			# Announce changes only if these changes are not related to switching to another chat
			if chat_name == last_value[0] and sub_title:
				# Replacing the symbol that interferes with the sounding of this element
				sub_title_name = sub_title.replace("‎∶‎", "‎:‎")
				queueHandler.queueFunction(queueHandler.eventQueue, message, sub_title_name)
			cls.last_value = (chat_name, sub_title)
		Timer(cls.interval, cls.tick).start()
	@classmethod
	def toggle(cls, app):
		if not config.conf["WhatsAppPlus"]["automatically announce activity in chats"]:
			cls.app = app
			cls.pouse = False
			cls.active = True
			config.conf["WhatsAppPlus"]["automatically announce activity in chats"] = True
			Timer(cls.interval, cls.tick).start()
			return True
		else:
			cls.active = False
			config.conf["WhatsAppPlus"]["automatically announce activity in chats"] = False
			return False
	@classmethod
	def restore(cls, app):
		cls.pouse = False
		cls.active = True
		cls.app = app
		cls.last_value = None
		Timer(cls.interval, cls.tick).start()


class Chat_update:
	active = False
	pouse = False
	interval = .4
	interval = .12
	app = False
	last_message = None
	
	@classmethod
	def tick(cls):
		if not cls.active or cls.pouse: return
		try :
			last_message = cls.app.get_messages_element().lastChild
			total_count_messages = last_message.positionInfo["similarItemsInGroup"]
			number_message = last_message.positionInfo["indexInGroup"]
		except:
			total_count_messages = None
			last_message = None
			number_message = None
		if not last_message or not total_count_messages or not number_message or not last_message.isInForeground:
			cls.pouse = True
			return True
		# The first element is the name of the chat in which the last message was received
		# We consider the chat name to be the name of the text field for entering messages, since the name of the field is different in each chat
		# The second item is the number of messages in the chat
		last_saved_message = cls.last_message or ("", "")
		if total_count_messages != last_saved_message[1] and total_count_messages == number_message:
			try:
				title = cls.app.message_box_element.name
			except:
				Timer(cls.interval, cls.tick).start()
				return False
			is_my_message = cls.app.is_message_contains_user_name(last_message.name) or cls.app.is_message_contains_phone_number(last_message.name)
			if title == last_saved_message[0] and is_my_message == False:
				cls.app.action_message_focus(last_message)
				text = last_message.name
				playWaveFile(baseDir+"whatsapp_incoming.wav")
				queueHandler.queueFunction(queueHandler.eventQueue, message, text)
			cls.last_message = (title, total_count_messages)
		Timer(cls.interval, cls.tick).start()
	
	@classmethod
	def toggle(cls, app):
		if not config.conf["WhatsAppPlus"]["automaticReadingOfNewMessages"]:
			config.conf["WhatsAppPlus"]["automaticReadingOfNewMessages"] = True
			cls.active = True
			cls.pouse = False
			cls.app = app
			Timer(cls.interval, cls.tick).start()
			return True
		else:
			config.conf["WhatsAppPlus"]["automaticReadingOfNewMessages"] = False
			cls.active = False
			return False
	
	@classmethod
	def restore(cls, app):
		cls.pouse = False
		cls.active = True
		cls.app = app
		cls.last_message = None
		Timer(cls.interval, cls.tick).start()


class FileDownloadIndicator:
	active = False
	interval = 1
	progress_object = None
	last_value = None
	def start():
		obj = api.getFocusObject()
		FileDownloadIndicator.progress_object = next(
			(item for item in obj.children if item.role == controlTypes.Role.PROGRESSBAR and item.next and item.next.name == "\ue711"), None)
		if FileDownloadIndicator.progress_object:
			FileDownloadIndicator.active = True
			FileDownloadIndicator.tick()
	def tick():
		obj = api.getFocusObject()
		if not FileDownloadIndicator.progress_object or not obj.UIAAutomationId or obj.UIAAutomationId != "BubbleListItem" or not FileDownloadIndicator.progress_object.location.left:
			FileDownloadIndicator.active = False
			FileDownloadIndicator.progress_object = None
			return False
		value = FileDownloadIndicator.progress_object.value or FileDownloadIndicator.progress_object.name or "Wait"
		if not FileDownloadIndicator.last_value or FileDownloadIndicator.last_value != value:
			message(value)
			FileDownloadIndicator.last_value = value
		Timer(FileDownloadIndicator.interval, FileDownloadIndicator.tick).start()


class AppModule(appModuleHandler.AppModule):
	scriptCategory = "WhatsAppPlus"
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.app_version = self.productVersion
		self.is_old_interface = False
		if int(str(self.app_version).replace(".", "")) < 2224010:
			self.is_old_interface = True
		config.conf.spec['WhatsAppPlus'] = SPEC
		# Launching the function of automatic announcement of new messages in an open chat
		if config.conf['WhatsAppPlus']['automaticReadingOfNewMessages'] and not Chat_update.active:
			Chat_update.restore(self)
		if config.conf['WhatsAppPlus']['automatically announce activity in chats'] and not Title_change_tracking.active:
			Title_change_tracking.restore(self)
	
	message_list_element = None
	last_focus_message_element = None
	chats_list_element = None
	last_focus_chat_element = None
	title_chat_element = None
	last_title_value = ""
	message_box_element = None
	execute_context_menu_option = None
	save_focus = None
	is_skip_name = 0
	rewind_slider = None

	def get_elements(self):
		# if not self.is_old_interface:
		try:
			return api.getForegroundObject().children[1].firstChild.children
		except:
		# else:
			return api.getForegroundObject().children[1].children
	
	def get_messages_element(self):
		obj = self.message_list_element
		if not obj or not obj.location:
			obj = next((item for item in self.get_elements() if item.UIAAutomationId == "MessagesList"), None)
			if obj: self.message_list_element = obj
		if obj and controlTypes.State.UNAVAILABLE not in obj.states: return obj
		else: return None

		obj = api.getFocusObject()
		if obj.role == controlTypes.Role.LISTITEM and obj.parent.UIAAutomationId == "ChatsList" and obj.location:
			message(obj.name)
			return
		if self.lastFocusSelectedChatElement and self.lastFocusSelectedChatElement.location and self.lastFocusSelectedChatElement.location.width:
			self.lastFocusSelectedChatElement.setFocus()
			return
		if self.lastFocusChatElement and self.lastFocusChatElement.location and self.lastFocusChatElement.location.width:
			self.lastFocusChatElement.setFocus()
			return
		targetList = self.chatListElement
		if not targetList or not targetList.location or not targetList.location.width:
			targetList = next((item for item in reversed(self.getElements()) if item.role == controlTypes.Role.TABCONTROL and item.UIAAutomationId == "rpMasterTitlebar"), False)
			if not targetList:
				if not arg: message(_("Chat list not found"))
				return False
			targetList = next((item for item in targetList.firstChild.children if item.role == controlTypes.Role.LIST and 	item.UIAAutomationId == "ChatsList"), False)
			if targetList: self.chatListElement = targetList
		return targetList

	def get_chats_element(self):
		obj = self.chats_list_element
		if not obj or (not obj.location.width):
			obj = next((item.firstChild for item in self.get_elements() if item.UIAAutomationId == "ChatList"), None)
			if obj: self.chats_list_element = obj
		return obj

		obj = api.getFocusObject()
		if obj.role == controlTypes.Role.LISTITEM and obj.parent.UIAAutomationId == "ChatsList" and obj.location:
			message(obj.name)
			return
		if self.lastFocusSelectedChatElement and self.lastFocusSelectedChatElement.location and self.lastFocusSelectedChatElement.location.width:
			self.lastFocusSelectedChatElement.setFocus()
			return
		if self.lastFocusChatElement and self.lastFocusChatElement.location and self.lastFocusChatElement.location.width:
			self.lastFocusChatElement.setFocus()
			return
		targetList = self.chatListElement
		if not targetList or not targetList.location or not targetList.location.width:
			targetList = next((item for item in reversed(self.getElements()) if item.role == controlTypes.Role.TABCONTROL and item.UIAAutomationId == "rpMasterTitlebar"), False)
			if not targetList:
				if not arg: message(_("Chat list not found"))
				return False
			targetList = next((item for item in targetList.firstChild.children if item.role == controlTypes.Role.LIST and 	item.UIAAutomationId == "ChatsList"), False)
			if targetList: self.chatListElement = targetList
		return targetList

	def get_title_element(self):
		self.title_chat_element = self.title_chat_element if self.title_chat_element and self.title_chat_element.location else next((item for item in self.get_elements() if controlTypes.State.FOCUSABLE in item.states and item.UIAAutomationId == "TitleButton"), None)
		return self.title_chat_element

	# Go to the last message in the chat
	@script(description=_("Move focus to the last message in an open chat"), gesture="kb:ALT+2")
	def script_toLastMessage(self, gesture):
		obj = api.getFocusObject()
		if obj.UIAAutomationId == "BubbleListItem":
			if obj.next: KeyboardInputGesture.fromName("end").send()
			else: message(obj.name)
			return
		list = self.get_messages_element()
		try:
			list.lastChild.setFocus()
		except:
			if not list: message(_("No open chat"))
			elif not list.lastChild: message(_("This chat is empty"))

	# Go to chat list	
	@script(description=_("Move focus to chat list"), gesture="kb:ALT+1")
	def script_toChatList(self, gesture, arg = False):
		obj = api.getFocusObject()
		if obj.UIAAutomationId == "ChatsListItem":
			message(obj.name)
			return
		if self.last_focus_chat_element and self.last_focus_chat_element.location:
			self.last_focus_chat_element.setFocus()
			return
		chats = self.get_chats_element()
		try:
			element = chats.next.firstChild
			# Processing the situation when the list of starred messages is open. In this list, the first item is not the list item, but the name of the list
			if element.role != controlTypes.Role.LISTITEM and element.next and element.next.role == controlTypes.Role.LISTITEM: element = element.next
			element.setFocus()
		except Exception as e:
			message(_("Chat list is empty"))
	
	# Go to "unread messages" label
	@script(description=_("Move focus to 'unread messages' label"), gesture="kb:ALT+3")
	def script_goToTheLastUnreadMessage(self, gesture):
		list = self.get_messages_element()
		try:
			element  = list.lastChild
		except:
			if not list: message(_("No open chat"))
			elif not list.lastChild: message(_("This chat is empty"))
			return False
		text = config.conf["WhatsAppPlus"]["phrasesOfUnreadMessages"].split(",")
		while element:
			if next((True for item in text if element.firstChild.name.endswith(item) ), False): break
			else: element = element.previous
		if element: element.setFocus()
		else: message(_("There are no unread messages in this chat"))
	
	# Changing the playback speed of a voice message
	@script(description=_("Increase/decrease the playback speed of voice messages"), gesture="kb:control+S")
	def script_voiceMessageAcceleration(self, gesture):
		if not self.rewind_slider:
			message(_("Nothing is playing right now"))
			return False
		obj = self.rewind_slider.parent
		button = next((item for item in obj.children if item.UIAAutomationId == "PlaybackSpeedButton"), None)
		if button:
			last_focus = api.getFocusObject()
			button.doAction()
			last_focus.setFocus()
		else:
			message(_("Nothing is playing right now"))

	# Play/pause voice message
	@script(description=_("Play/pause the voice message currently playing"), gesture="kb:ALT+P")
	def script_pauseVoiceMessage(self, gesture):
		if not self.rewind_slider or self.rewind_slider.value == "0":
			message(_("Nothing is playing right now"))
			return False
		obj = self.rewind_slider.parent
		button = next((item for item in obj.children if item.UIAAutomationId == "IconTextBlock"), None)
		if button:
			p = button.location.center
			winUser.setCursorPos(p.x, p.y)
			mouseHandler.executeMouseEvent(winUser.MOUSEEVENTF_LEFTDOWN, 0, 0)
			mouseHandler.executeMouseEvent(winUser.MOUSEEVENTF_LEFTUP, 0, 0)
		else: message(_("Nothing is playing right now"))

	# Read profile name and status in open chat
	@script(description=_("Announce the name and status of an open chat"), gesture="kb:ALT+T")
	def script_read_profile_name(self, gesture):
		if scriptHandler.getLastScriptRepeatCount() == 1:
			if Title_change_tracking.toggle(self): message(_("Chat activity tracking is enabled"))
			else: message(_("Chat activity tracking is disabled"))
			return
		title = self.get_title_element()
		if title and controlTypes.State.FOCUSABLE in title.states:
			title = "\n".join([item.name for item in title.children])
			# Replacing the symbol that interferes with the sounding of this element
			title = title.replace("‎∶‎", "‎:‎")
			message(title)
		else: message(_("No open chat"))

	@script(description=_("Open current chat profile"), gesture="kb:control+shift+P")
	def script_openProfile(self, gesture):
		title = self.title_chat_element
		if not self.title_chat_element: self.title_chat_element = next((item for item in self.get_elements() if controlTypes.State.FOCUSABLE in item.states and item.UIAAutomationId == "TitleButton"), None)
		try: self.title_chat_element.doAction()
		except: message(_("No open chat"))

	# Перенести фокус в поле вводу повідомлення. Якщо фокус вже знаходиться в цьому полі, тоді перенести його на останній елемент який був в фокусі перед цим полемMove the focus to the edit field. If the focus is already in this field, then move it to the last element that had focus before this field
	@script(description=_("Move the focus to the edit field. If the focus is already in the edit field, then after pressing the hotkey, it will move to where it was before"), gesture="kb:ALT+D")
	def script_to_message_box(self, gesture, arg = False):
		obj = api.getFocusObject()
		if obj.UIAAutomationId == "InputBarTextBox" and self.last_focus_message_element:
			self.last_focus_message_element.setFocus()
			return
		message_box = self.message_box_element
		if not message_box:
			message_box = next((item for item in self.get_elements() if item.UIAAutomationId == "InputBarTextBox"), None)
			if message_box: self.message_box_element = message_box
		try:
			if message_box: message_box.setFocus()
		except:
			self.message_box_element = False
			self.script_to_message_box(gesture)

	# Copy current message to clipboard
	@script(description=_("Copy the message if it contains text"), gesture="kb:control+C")
	def script_copyMessage(self, gesture):
		obj = api.getFocusObject()
		if obj.UIAAutomationId != "BubbleListItem":
			gesture.send()
			return
		try: text = next((item.name for item in obj.children if item.UIAAutomationId == "TextBlock" and item.next.next.UIAAutomationId == "ReadMore"), None)
		except: text = None
		if text:
			api.copyToClip(text.strip())
			message(_("Message copied"))
		else: message(_("This message contains no text"))

	# Show message text in popup window
	@script(description=_("Show message text in popup window"), gesture="kb:ALT+C")
	def script_show_text_message(self, gesture):
		gesture.send()
		obj = api.getFocusObject()
		if obj.UIAAutomationId != "BubbleListItem": return
		try: text = next((item.name for item in obj.children if item.UIAAutomationId == "TextBlock" and item.next.next.UIAAutomationId == "ReadMore"), None)
		except: text = None
		if text: TextWindow(text.strip(), _("message text"), readOnly=False)
		else: message(_("This message contains no text"))

	# Call if it's a contact, or enter a voice chat if it's a group
	@script(description=_("Make a voice call"), gesture="kb:shift+alt+C")
	def script_call(self, gesture):
		button = next((item for item in self.get_elements() if item.UIAAutomationId == "AudioCallButton" and controlTypes.State.FOCUSABLE in item.states), None)
		if button: button.doAction()
		else: message(_("Call unavailable"))

	# Make a video call if it's a contact
	@script(description=_("Make a video call"), gesture="kb:shift+alt+V")
	def script_videoCall(self, gesture):
		button = next((item for item in self.get_elements() if item.UIAAutomationId == "VideoCallButton" and controlTypes.State.FOCUSABLE in item.states), None)
		if button: button.doAction()
		else: message(_("Video call not available"))

	# End or decline call
	# @script(description=_("Press \"Decline call\" button  if there is an incoming call or \"End call\" button if a call is in progress"), gesture="kb:ALT+shift+N")
	def script_callCancellation(self, gesture):
		elements = api.getForegroundObject().children[1].firstChild.children
		button = next((item for item in elements if item.role == controlTypes.Role.BUTTON and item.firstChild.name == "\ue65a"), None)
		if button: button.doAction()

	# Mute/unmute the microphone
	@script(description=_("Mute or unmute the microphone"), gesture="kb:ALT+A")
	def script_microphone(self, gesture):
		elements = api.getForegroundObject().children[1].firstChild.children
		button = next((item for item in elements if item.role == controlTypes.Role.BUTTON and item.UIAAutomationId == "MicMuteButton"), None)
		if not button: return
		focus = api.getFocusObject()
		button.doAction()
		focus.setFocus()
		def announce_name_button(): message(button.name)
		Timer(.2, announce_name_button).start()

	# Turn on/off the camera
	@script(description=_("Turn the camera on and off"), gesture="kb:ALT+V")
	def script_video(self, gesture):
		elements = api.getForegroundObject().children[1].firstChild.children
		button = next((item for item in elements if item.role == controlTypes.Role.BUTTON and item.UIAAutomationId == "ActivateVideoButton"), None)
		if not button: return
		focus = api.getFocusObject()
		button.doAction()
		focus.setFocus()
		def announce_name_button(): message(button.name)
		Timer(.2, announce_name_button).start()

	# Press the "Attach media" button
	@script(description=_("Press \"Attach file\" button"), gesture="kb:control+shift+A")
	def script_add_files(self, gesture):
		button = next((item for item in self.get_elements() if controlTypes.State.FOCUSABLE in item.states and item.UIAAutomationId == "AttachButton"), None)
		if button: button.doAction()
		else: message(_("Button not found"))

		# Press the "New conversation" button
	
	# Press the "More options" button
	@script(description=_("Press \"More Options\" button"), gesture="kb:ALT+O")
	def script_showMoreOptions(self, gesture):
		button = next((item for item in self.get_elements() if item.role == controlTypes.Role.BUTTON and item.UIAAutomationId == "SettingsButton"), None)
		if button: button.doAction()
		else: message(_("Button not found"))

	# Function of recording and sending a voice message
	@script(description=_("Record and send a voice message"), gesture="kb:control+R")
	def script_recordingVoiceMessage(self, gesture):
		button = next((item for item in self.get_elements() if item.role == controlTypes.Role.BUTTON and controlTypes.State.FOCUSABLE in item.states and item.UIAAutomationId in ("RightButton", "SendVoiceMessageButton")), None)
		if not button:
			return
		if button.UIAAutomationId == "RightButton":
			if button.firstChild.name == "\ue724":
				# If the edit field is not empty
				message(_("Recording a voice message will not be available until the edit field is empty"))
				return
			if config.conf["WhatsAppPlus"]['playSoundWhenRecordingVoiceMessage']:
				playWaveFile(baseDir+"wa_ptt_start_record.wav")
			self.is_skip_name = 2
			button.doAction()
		elif button.UIAAutomationId == "SendVoiceMessageButton":
			self.is_skip_name = 2
			button.doAction()
			if config.conf["WhatsAppPlus"]['playSoundWhenRecordingVoiceMessage']:
				playWaveFile(baseDir+"wa_ptt_sent.wav")

	# Voice message discard function
	@script(description=_("Discard voice message"), gesture="kb:control+D")
	def script_cancelVoiceMessageRecording(self, gesture):
		button = next((item for item in self.get_elements() if (item.role == controlTypes.Role.BUTTON and controlTypes.State.FOCUSABLE in item.states and item.UIAAutomationId == "PttDeleteButton") or (item.firstChild and item.firstChild.name == "\ue8bb")), None)
		if not button: return
		if button.UIAAutomationId == "PttDeleteButton":
			if config.conf["WhatsAppPlus"]['playSoundWhenRecordingVoiceMessage']:
				playWaveFile(baseDir+"wa_ptt_quick_cancel.wav")
			self.is_skip_name = 1
			button.doAction()
		elif button.firstChild and button.firstChild.name == "\ue8bb":
			focus = api.getFocusObject()
			button.doAction()
			focus.setFocus()
			message(_("Reply canceled"))
	
	# Voice message recording pause function
	@script(description=_("Pause/resume voice message recording"), gesture="kb:control+shift+d")
	def script_stopVoiceMessageRecording(self, gesture):
		button = next((item for item in self.get_elements() if item.role == controlTypes.Role.BUTTON and controlTypes.State.FOCUSABLE in item.states and item.UIAAutomationId in ("PttPauseButton", "PttResumeButton")), None)
		if not button: return
		if button.UIAAutomationId == "PttPauseButton":
			if config.conf["WhatsAppPlus"]['playSoundWhenRecordingVoiceMessage']:
				playWaveFile(baseDir+"wa_ptt_stop_record.wav")
			self.is_skip_name = 1
			button.doAction()
		elif button.UIAAutomationId == "PttResumeButton":
			if config.conf["WhatsAppPlus"]['playSoundWhenRecordingVoiceMessage']:
				playWaveFile(baseDir+"wa_ptt_start_record.wav")
			self.is_skip_name = 1
			button.doAction()

	def activate_option_for_menu(self, option):
		obj = api.getFocusObject()
		if self.execute_context_menu_option or obj.UIAAutomationId not in ("BubbleListItem", "ChatsListItem"): return
		if isinstance(option, str): option = (option,)
		self.execute_context_menu_option = option
		KeyboardInputGesture.fromName("Applications").send()

	@script(description=_("Forward message"), gesture="kb:ALT+F")
	def script_forwardMessage(self, gesture):
		self.activate_option_for_menu(icon_from_context_menu["forward message"])
	# @script(description=_("React to message"), gesture="kb:ALT+Q")
	# def script_set_reaction(self, gesture):
		# self.activate_option_for_menu(icon_from_context_menu["react"])
	@script(description=_("Delete a message or chat"), gesture="kb:ALT+delete")
	def script_deletion(self, gesture):
		self.activate_option_for_menu(icon_from_context_menu["delete"])
	@script(description=_("Reply to message"), gesture="kb:ALT+R")
	def script_reply_to_message(self, gesture):
		self.activate_option_for_menu(icon_from_context_menu["reply to message"])
	@script(description=_("Edit message"), gesture="kb:ALT+backspace")
	def script_edit_message(self, gesture):
		self.activate_option_for_menu(icon_from_context_menu["edit message"])
	@script(description=_("Mark a chat as read"), gesture="kb:ALT+shift+R")
	def script_read_chat(self, gesture):
		self.activate_option_for_menu((icon_from_context_menu["mark as read"], icon_from_context_menu["mark as unread"]))
	@script(description=_("Star message"), gesture="kb:ALT+S")
	def script_Star_message(self, gesture):
		self.activate_option_for_menu((icon_from_context_menu["star message"], icon_from_context_menu["видалити з обраних"]))
	@script(description=_("Save file as..."))
	def script_save_file(self, gesture):
		self.activate_option_for_menu(icon_from_context_menu["save as"])
	def script_action_space(self, gesture):
		obj = api.getFocusObject()
		try: obj.UIAAutomationId
		except: gesture.send()
		if obj.UIAAutomationId != "BubbleListItem":
			gesture.send()
			return
		def perevirka(item):
			return item.name in ("\uf5b0", "\ue769") or (item.firstChild and item.firstChild.role == controlTypes.Role.LINK)
		button = next((item for item in obj.children if perevirka(item)), None)
		if button:
			p = button.location.center
			winUser.setCursorPos(p.x, p.y)
			mouseHandler.executeMouseEvent(winUser.MOUSEEVENTF_LEFTDOWN, 0, 0)
			mouseHandler.executeMouseEvent(winUser.MOUSEEVENTF_LEFTUP, 0, 0)
		else: gesture.send()
	def script_back(self, gesture):
		button = next((item for item in self.get_elements() if item.role == controlTypes.Role.BUTTON and item.UIAAutomationId in ("BackButton", "CloseButton")), None)
		if button:
			message(_("Back"))
			button.doAction()
		else: message(_("Button not found"))

	# Switching the mode of deleting a phone number in contact names	
	@script(description=_("Toggles the mode that removes the reading of the user number when reading messages that are not in the contact list"), gesture="kb:control+shift+E")
	def script_save_as(self, gesture):
		config.conf["WhatsAppPlus"]["displayPhoneNumberInUsername"] = not config.conf["WhatsAppPlus"]["displayPhoneNumberInUsername"]
		if config.conf["WhatsAppPlus"]["displayPhoneNumberInUsername"]: message(_("User numbers will be read"))
		else: message(_("User numbers will not be read"))

	@script(description=_("Enable automatic reading of new messages in the current chat"), gesture="kb:ALT+L")
	def script_toggle_live_chat(self, gesture):
		if Chat_update.toggle(self): message(_("Automatic reading of messages is enabled"))
		else: message(_("Automatic reading of new messages is disabled"))

	@script(description=_("Announce the current value of the progress bar. When double-pressed, turns on/off the automatic sounding of performance indicators."), gesture="kb:ALT+U")
	def script_announce_progress_bar(self, gesture):
		if scriptHandler.getLastScriptRepeatCount() == 1:
			config.conf["WhatsAppPlus"]["automatically_report_progress_indicators"] = not config.conf["WhatsAppPlus"]["automatically_report_progress_indicators"]
			if config.conf["WhatsAppPlus"]["automatically_report_progress_indicators"]: message(_("Now the values ​​of the performance indicators will be announced automatically"))
			else: message(_("Now the values ​​of the progress indicators will not be announced automatically"))
			return
		obj = api.getFocusObject()
		if obj.UIAAutomationId == "BubbleListItem":
			progress = next((item for item in obj.children if item.role == controlTypes.Role.PROGRESSBAR and (item.value or item.name)), None)
			if progress: message(progress.value or progress.name)
			else: message(_("This message does not include a progress bar"))
		else: message(_("This element is not a message"))

	@script(description=_("Switch to selection mode"), gesture="kb:control+space")
	def script_selectMessage(self, gesture):
		self.activate_option_for_menu(icon_from_context_menu["select message"])

	@script(description=_("Show a list of all whatsAppPlus shortcuts"), gesture="kb:ALT+H")
	def script_help(self, gesture):
		a = next((item for item in list(addonHandler.getAvailableAddons()) if item.name == "whatsAppPlus"), None)
		a = a.getDocFilePath()
		# We replace the file extension, because we need an md file
		a = a[:-4]+"md"
		with open(a, "r", encoding="utf-8") as file:
			text = file.read()
		blocks = text.split("\n\n")
		count_rows = [len(item.split("\n")) for item in blocks]
		index = count_rows.index(max(count_rows))
		text = blocks[index]
		text = text.replace("* ", "")
		text = text.replace("## ", "")
		TextWindow(text.strip(), _("List of shortcuts"), readOnly=True)

	def is_message_contains_user_name(self, text_message):
		if not config.conf["WhatsAppPlus"]["user_name"]: return False
		if text_message.startswith(config.conf["WhatsAppPlus"]["user_name"]):
				return config.conf["WhatsAppPlus"]["user_name"]
		else: return False
	
	def is_message_contains_phone_number(self, text_message):
		if not config.conf["WhatsAppPlus"]["number_phone"]: return False
		number_in_message = text_message.split(":")[0]
		cleaned_phone = sub(r"[^\d+]", "", number_in_message)
		number_phome = config.conf["WhatsAppPlus"]["number_phone"]
		numbers = number_phome.split("|")
		for number in numbers:
			if number in cleaned_phone:
				return number_in_message
				break
		else:
			return False

	# Processing the message that got into focus
	def action_message_focus(self, obj):
		number_in_message = self.is_message_contains_user_name(obj.name) or self.is_message_contains_phone_number(obj.name)
		reactions = ""
		answer = False
		duration = False
		time_element = False
		# Save reply text if message was written as a reply to a message
		text = False
		for item in obj.children:
			if item.UIAAutomationId == "Text": text = item
			elif item.UIAAutomationId == "TextBlock" and item.next and item.next.UIAAutomationId in ("ReadMore", "Scrubber"):
				time_element = item.name
				item = item.previous
				try:
					if text and obj.firstChild.UIAAutomationId in ("", "NameTextBlock"):
						# Saving a username to remove from a message
						name = obj.children[0]
						# Saving the username to be added at the end of the message
						new_name = text.previous
						# If a user with a phone number replies to a message with a link
						if new_name.previous and new_name.previous.UIAAutomationId == "PushNameTextBlock": name =new_name
						answer = (name.name, new_name.name, text.name.strip())
				except: pass
			elif item.UIAAutomationId == 'ReactionBubble':
				reactions = item.name
			elif item.UIAAutomationId == "Duration": duration = item.name
			elif item.UIAAutomationId == "TitleTextBlock"and " http" in obj.name:
				# If the message contains a link, then try to display the description of that link
				obj.name = obj.name.replace("http", item.name+", "+"http")

		if obj.name.endswith(" "): obj.name = obj.name[:-1]
		if answer:
			obj.name = sub(r" {} ({})?".format(escape(answer[0]), escape(answer[2])), "", obj.name)
			obj.name += ".\n"+_("In response to")+": "+answer[1]+", "+answer[2]
		if not time_element and (obj.children[0].UIAAutomationId == "Icon" or (obj.childCount > 1 and obj.children[1].UIAAutomationId == "Icon")):
			item = obj.children[0]
			if obj.children[0].UIAAutomationId != "Icon": item = item.next
			new_name = item.next.name+", "+item.next.next.name
			obj.name = sub(r" (\w{2,12}) {1,3}(\d\d:\d\d)", r" \1 %s \2"%new_name, obj.name)
		if duration: obj.name = obj.name.replace("   ", " "+duration+", ")
		if reactions: obj.name += ".\n"+reactions
		# Remove my phone number from my messages
		if number_in_message:
			obj.name = obj.name.replace(number_in_message, _("You"), 1)
		# Add a file name to the message
		if obj.firstChild.UIAAutomationId == "Icon" and obj.firstChild.next.UIAAutomationId == "NameTextBlock":
			file_name = f"{obj.firstChild.next.name}, {obj.firstChild.next.next.name}"
			obj.name = sub(" (‎\d\d?‎∶‎\d\d?)", f"{file_name}, \g<1>", obj.name)
		# Remove phone number from usernames
		if not config.conf["WhatsAppPlus"]["displayPhoneNumberInUsername"]: obj.name = sub(reg_for_delete_phon_number, '', obj.name)
		# Replacing the symbol that interferes with the sounding of this element
		obj.name = obj.name.replace("‎∶‎", "‎:‎")

		if controlTypes.State.SELECTED in obj.states: message(_("Selected"))
	
	__gestures = {
		"kb:space": "action_space",
		"kb:ALT+leftArrow": "back",
	}


	def event_gainFocus(self, obj, nextHandler):
		if config.conf['WhatsAppPlus']['automaticReadingOfNewMessages'] and Chat_update.pouse:
			Chat_update.restore(self)
		if config.conf['WhatsAppPlus']['automatically announce activity in chats'] and Title_change_tracking.pouse:
			Title_change_tracking.restore(self)
		if self.is_skip_name:
			speech.cancelSpeech()
			self.is_skip_name -= 1
			return
		elif self.save_focus:
			self.save_focus.setFocus()
			self.save_focus = None
			self.is_skip_name = True
			return
		elif self.execute_context_menu_option:
			if obj.parent.UIAAutomationId == "EmojiList": obj = obj.parent.parent
			try: targetButton = next((item for item in obj.parent.children if item.firstChild.name in self.execute_context_menu_option), None)
			except: targetButton = None
			self.execute_context_menu_option = False
			if targetButton: targetButton.doAction()
			else: KeyboardInputGesture.fromName("escape").send()
			return
		if obj.role == controlTypes.Role.LISTITEM and obj.UIAAutomationId:
			if obj.UIAAutomationId == "BubbleListItem":
				speech.cancelSpeech()
				self.last_focus_message_element = obj
				self.action_message_focus(obj)
				if config.conf["WhatsAppPlus"]["automatically_report_progress_indicators"]: FileDownloadIndicator.start()
			elif obj.UIAAutomationId == "ChatsListItem":
				speech.cancelSpeech()
				self.last_focus_chat_element = obj
		elif obj.role == controlTypes.Role.EDITABLETEXT and obj.UIAAutomationId == "InputBarTextBox":
			obj.description = ""
			try:
				if obj.previous.previous.previous.firstChild.name == "\ue8bb":
					answer_to = obj.previous.previous.previous.previous.previous
					if answer_to.UIAAutomationId == "Text": answer_to = answer_to.previous
					obj.name = _("Answer to")+": "+answer_to.name
			except: pass
		elif obj.role == controlTypes.Role.COMBOBOX:
			if obj.UIAAutomationId == "ThemeCombobox": obj.name = obj.previous.name +": "+ obj.firstChild.lastChild.name
		nextHandler()


	# Processing item initialization
	# def chooseNVDAObjectOverlayClasses(self, obj, clsList):
	def event_NVDAObject_init(self,obj):
		try:
			if obj.role == controlTypes.Role.LISTITEM:
				parent = obj.parent
				if obj.name == "WhatsApp.CleanViewModels.LightBox.ItemVm.LightBoxExtendedTextItemVm" and obj.firstChild:
					# A caption for a text-only story
					obj.name = obj.firstChild.name
				elif obj.name in ('WhatsApp.CallParticipantVm', 'WhatsApp.SelfStreamVm', 'WhatsApp.RecipientItem', 'WhatsApp.ReceiptViewModel'):
					obj.name = ", ".join([m.name for m in obj.children])
				elif obj.name == 'WhatsApp.Design.LightBoxExtendedTextItemVm':
					obj.name = obj.firstChild.name
				elif obj.name == 'WhatsApp.Design.ThemeData':
					obj.name = obj.children[1].name
				elif controlTypes.State.SELECTED in obj.states and obj.parent.UIAAutomationId in ("EmojiList", "MentionsList"):
					# Reading the name of the selected user in the list with hints when typing the @ symbol
					queueHandler.queueFunction(queueHandler.eventQueue, message, obj.name)
				elif obj.name == "WhatsApp.Design.CallHistoryListCellVm":
					# We sign the list items in the "Calls" section
					obj.name = ", ".join([item.name for item in obj.firstChild.children if item.name])
				if obj.UIAAutomationId == "" and parent.UIAAutomationId == "FlipView" and obj.firstChild.role == controlTypes.Role.GROUPING:
					# Caption for statuses that contain images or videos
					obj.name = parent.next.next.next.next.name+ "\n" + obj.name
			elif obj.role == controlTypes.Role.BUTTON:
				if obj.name == "\ue8bb": obj.name = _("Cancel reply")
				elif obj.UIAAutomationId == "CloseButton": obj.name = _("Close")
				elif obj.UIAAutomationId == "MuteDropdown": obj.name = obj.lastChild.name
				elif obj.UIAAutomationId == 'SendMessages': obj.name = '{}: {}'.format(obj.previous.name, obj.firstChild.name)
				elif obj.UIAAutomationId == 'EditInfo': obj.name = '{}: {}'.format(obj.previous.name, obj.firstChild.name)
				elif obj.UIAAutomationId in ('CancelButton', 'RejectButton'): obj.name = obj.firstChild.name
				elif obj.UIAAutomationId == "PlusButton": obj.name = _("Add")
				elif obj.UIAAutomationId == "StarButton" and obj.name == "\ue734": obj.name = _("Star")
				elif obj.UIAAutomationId == "StarButton" and obj.name == "\ue735": obj.name = _("Unstar")
				elif obj.UIAAutomationId == "ReactionButton": obj.name = _("React to message")
				elif obj.UIAAutomationId == "NextButton": obj.name = _("Next")
				elif obj.UIAAutomationId == "PreviousButton": obj.name = _("Previous")
				elif obj.name == "\ue74f": obj.name = _("Mute")
				elif obj.name == "\ue767": obj.name = _("Unmute")
				elif obj.name == "\ue769": obj.name = _("Pause")
				elif obj.name == "\uf5b0": obj.name = _("Play")
				elif obj.UIAAutomationId == "CopyButton": obj.name = _("Copy")
				elif obj.UIAAutomationId == "ForwardButton": obj.name = _("Forward")
				elif obj.UIAAutomationId == "DeleteButton": obj.name = _("Delete")
			elif obj.role == controlTypes.Role.TOGGLEBUTTON:
				if obj.UIAAutomationId in ("WhenWAClosedSwitch", "NewMessagesNotificationSwitch"): obj.name = obj.previous.name
			elif obj.role == controlTypes.Role.GROUPING:
				if obj.name in ('WhatsApp.ViewModels.EmojiPickerCategoryViewModel', 'WhatsApp.Pages.Recipients.RecipientGroupingVm`1[WhatsApp.Pages.Recipients.NewChatVm+IItem]', 'WhatsApp.Pages.Recipients.RecipientGroupingVm`1[WhatsApp.Pages.Recipients.ForwardMessageVm+IItem]', 'WhatsApp.Pages.Recipients.RecipientGroupingVm`1[WhatsApp.AddCallParticipantsVm+IItem]', 'WhatsApp.Pages.Recipients.UserRecipientItemVm'):
					obj.name = obj.firstChild.name
			elif obj.role == controlTypes.Role.CHECKBOX:
				# if obj.UIAAutomationId == "Scrubber" and obj.value != "0" and obj.location.left: self.rewind_slider = obj
				if obj.name == "" and obj.childCount == 3 and obj.parent.UIAAutomationId == "BubbleListItem":
					# We sign the answer options in the surveys
					obj.name = obj.firstChild.name+", "+obj.children[1].name+" votes"+obj.lastChild.value
			elif obj.role == controlTypes.Role.EDITABLETEXT and obj.UIAAutomationId == "InputBarTextBox":
				self.message_box_element = obj
		except: pass

	def event_valueChange(self, obj, nextHandler):
		if obj.UIAAutomationId == "Scrubber" and obj.value != "0" and obj.location.left:
			self.rewind_slider = obj
		nextHandler()
