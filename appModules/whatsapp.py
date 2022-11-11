import appModuleHandler
import api
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
# reg_time_message = compile(r"?\s?\d\d:\d\d\s??")

baseDir = os.path.join(os.path.dirname(__file__), "media\\")

addonHandler.initTranslation()

icon_from_context_menu = {
	"відповісти на повідомлення": "\ue97a",
	"встановити реакцію": "\ue76e",
	"переслати повідомлення": "\uee35",
	"видалити": "\ue74d",
	"помітити як прочитаний": "\ue8bd",
	"позначити як непрочитаний": "\ue668",
	"покинути групу": "\ue89b",
	"добавити в обрані": "\ue734",
	"видалити з обраних": "\ue735",
	"зберегти як": "\ue74e"
}

lang = languageHandler.getLanguage().split("_")[0]

phrases_of_unread_messages = {
	"uk": "непрочитані повідомлення,непрочитаних повідомлень, непрочитане повідомлення",
	"tr": "okunmamış mesaj",
	"es": "mensajes no leídos",
	"it": "messaggi non letti,messaggio non letto",
	"en": "unread messages,unread message",
	"ro": "mesaje necitite",
	"sr": "nepročitane poruke",
	"hr": "nepročitanih poruka,nepročitane poruke,nepročitana poruka",
}

SPEC = {
	'playSoundWhenRecordingVoiceMessage': 'boolean(default=False)',
	'phrasesOfUnreadMessages': 'string(default="'+phrases_of_unread_messages.get(lang, "en")+'")',
	'isAutomaticallyCheckForUpdates': 'boolean(default=True)',
	'displayPhoneNumberInUsername': 'boolean(default=True)',
	'automaticReadingOfNewMessages': 'boolean(default=False)',
}

class Chat_update:
	active = False
	interval = .3
	app = False
	last_message = ("", "")
	def tick():
		if not Chat_update.active: return
		try : last_message = Chat_update.app.get_messages_element().lastChild
		except: last_message = False
		# Перший елемент це назва чату, в якому було зафіксовано останнє повідомлення
		# Другий елемент це індекс повідомлення
		last_saved_message = Chat_update.last_message
		# Якщо є проблеми з отриманням індекса повідомлення, тоді ми завершуємо функцію і викликаємо наступну ітерацію
		try:
			last_message.positionInfo["indexInGroup"]
			last_message.positionInfo["similarItemsInGroup"]
		except:
			Timer(Chat_update.interval, Chat_update.tick).start()
			return
		if last_message.isInForeground and last_message and last_message.positionInfo["indexInGroup"] != last_saved_message[1] and last_message.positionInfo["indexInGroup"] == last_message.positionInfo["similarItemsInGroup"]:
			try:
				title = Chat_update.app.get_title_element().firstChild.next.name
			except:
				Timer(Chat_update.interval, Chat_update.tick).start()
				return False
			parent = Chat_update.app.get_messages_element()
			is_message_received = True if last_message.location.left - parent.location.left < 40 else False
			if (title == last_saved_message[0]) and is_message_received:
				Chat_update.app.action_message_focus(last_message)
				text = last_message.name
				playWaveFile(baseDir+"whatsapp_incoming.wav")
				queueHandler.queueFunction(queueHandler.eventQueue, message, text)
			try:
				new_message = (title, last_message.positionInfo["indexInGroup"])
				Chat_update.last_message = new_message
			except: pass
		Timer(Chat_update.interval, Chat_update.tick).start()
	def toggle(app, active=None):
		if not Chat_update.active and (active or active == None):
			Chat_update.active = True
			Chat_update.app = app
			Timer(Chat_update.interval, Chat_update.tick).start()
			return True
		else:
			Chat_update.active = False
			return False


class AppModule(appModuleHandler.AppModule):
	scriptCategory = "WhatsAppPlus"
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.app_version = self.productVersion
		self.is_old_interface = False
		if int(str(self.app_version).replace(".", "")) < 2224010:
			self.is_old_interface = True
		# Запускаємо функцію автоматичного озвучення нових повідомлень у відкритому чаті
		config.conf.spec['WhatsAppPlus'] = SPEC
		if not Chat_update.active:
			Chat_update.toggle(self, config.conf['WhatsAppPlus']['automaticReadingOfNewMessages'])
	
	message_list_element = None
	last_focus_message_element = None
	chats_list_element = None
	last_focus_chat_element = None
	title_chat_element = None
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
		if not obj:
			obj = next((item for item in self.get_elements() if item.UIAAutomationId == "ListView"), None)
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
		if not obj or (obj and not obj.location.width):
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
		self.title_chat_element = self.title_chat_element or next((item for item in self.get_elements() if controlTypes.State.FOCUSABLE in item.states and item.UIAAutomationId == "TitleButton"), None)
		return self.title_chat_element

	# Перейти до останнього повідомлення в чаті
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

	# Перейти до списку чатів	
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
			element = chats.firstChild
			# Обробляємо ситуацію, коли відкритий список обраних повідомлень. В цьому списку першим елементом є не елемент списку, а назва списку
			if element.role != controlTypes.Role.LISTITEM and element.next and element.next.role == controlTypes.Role.LISTITEM: element = element.next
			element.setFocus()
		except: message(_("Chat list is empty"))
	
	# Перейти до мітки "непрочитані повідомлення"
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
	
	# Зміна швидкості відтворення голосового повідомлення
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
		else: message(_("Nothing is playing right now"))

	# Призупинити відтворення голосового повідомлення
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

	# Озвучує назву і статус профілю, в відкритому чаті
	@script(description=_("Announce the name and status of an open chat"), gesture="kb:ALT+T")
	def script_read_profile_name(self, gesture):
		title = self.get_title_element()
		if title and controlTypes.State.FOCUSABLE in title.states:
			title = "\n".join([item.name for item in title.children])
			message(title)
		else: message(_("No open chat"))

	@script(description=_("Open current chat profile"), gesture="kb:control+shift+P")
	def script_openProfile(self, gesture):
		title = self.title_chat_element
		if not self.title_chat_element: self.title_chat_element = next((item for item in self.get_elements() if controlTypes.State.FOCUSABLE in item.states and item.UIAAutomationId == "TitleButton"), None)
		try: self.title_chat_element.doAction()
		except: message(_("No open chat"))

	# Перенести фокус в поле вводу повідомлення. Якщо фокус вже знаходиться в цьому полі, тоді перенести його на останній елемент який був в фокусі перед цим полем
	@script(description=_("Move the focus to the edit field. If the focus is already in the edit field, then after pressing the hotkey, it will move to where it was before"), gesture="kb:ALT+D")
	def script_to_message_box(self, gesture, arg = False):
		obj = api.getFocusObject()
		if obj.UIAAutomationId == "TextBox" and self.last_focus_message_element:
			self.last_focus_message_element.setFocus()
			return
		message_box = self.message_box_element
		if not message_box:
			message_box = next((item for item in self.get_elements() if item.UIAAutomationId == "TextBox"), None)
			if message_box: self.message_box_element = message_box
		try:
			if message_box: message_box.setFocus()
		except:
			self.message_box_element = False
			self.script_to_message_box(gesture)

	# Скопіювати поточне повідомлення в буфер обміну
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

	# Показати текст повідомлення в спливаючому вікні
	@script(description=_("Show message text in popup window"), gesture="kb:ALT+C")
	def script_show_text_message(self, gesture):
		gesture.send()
		obj = api.getFocusObject()
		if obj.UIAAutomationId != "BubbleListItem": return
		try: text = next((item.name for item in obj.children if item.UIAAutomationId == "TextBlock" and item.next.next.UIAAutomationId == "ReadMore"), None)
		except: text = None
		if text: TextWindow(text.strip(), _("message text"), readOnly=False)
		else: message(_("This message contains no text"))

	# Зателефонувати якщо це контакт, або увійти до голосового чату, якщо це група
	@script(description=_("Make a voice call"), gesture="kb:shift+alt+C")
	def script_call(self, gesture):
		button = next((item for item in self.get_elements() if item.UIAAutomationId == "AudioCallButton" and controlTypes.State.FOCUSABLE in item.states), None)
		if button: button.doAction()
		else: message(_("Call unavailable"))

	# Зателефонувати по відеозв'язку якщо це контакт
	@script(description=_("Make a video call"), gesture="kb:shift+alt+V")
	def script_videoCall(self, gesture):
		button = next((item for item in self.get_elements() if item.UIAAutomationId == "VideoCallButton" and controlTypes.State.FOCUSABLE in item.states), None)
		if button: button.doAction()
		else: message(_("Video call not available"))

	# Відповідь на дзвінок
	@script(description=_("Accept call"), gesture="kb:ALT+Y")
	def script_answeringCall(self, gesture):
		elements = api.getForegroundObject().children[1].firstChild.children
		button = next((item for item in elements if item.role == controlTypes.Role.BUTTON and item.firstChild.name == "\ue717"), None)
		if button: button.doAction()

	# Завершити дзвінок або відхилити дзвінок
	@script(description=_("Press \"Decline call\" button  if there is an incoming call or \"End call\" button if a call is in progress"), gesture="kb:ALT+N")
	def script_callCancellation(self, gesture):
		elements = api.getForegroundObject().children[1].firstChild.children
		button = next((item for item in elements if item.role == controlTypes.Role.BUTTON and item.firstChild.name == "\ue65a"), None)
		if button: button.doAction()

	# Вимкнення/увімкнення мікрофону
	@script(description=_("Mute or unmute the microphone"), gesture="kb:ALT+A")
	def script_microphone(self, gesture):
		elements = api.getForegroundObject().children[1].firstChild.children
		button = next((item for item in elements if item.role == controlTypes.Role.CHECKBOX and item.UIAAutomationId == "MicMuteButton"), None)
		if not button: return
		focus = api.getFocusObject()
		if controlTypes.State.CHECKED in button.states: message(_("Microphone on"))
		else: message(_("Microphone off"))
		button.doAction()
		focus.setFocus()

	# Вимкнення/увімкнення камери
	@script(description=_("Turn the camera on and off"), gesture="kb:ALT+V")
	def script_video(self, gesture):
		elements = api.getForegroundObject().children[1].firstChild.children
		button = next((item for item in elements if item.role == controlTypes.Role.CHECKBOX and item.UIAAutomationId == "VideoMuteButton"), None)
		if not button: return
		focus = api.getFocusObject()
		if controlTypes.State.CHECKED in button.states: message(_("Camera on"))
		else: message(_("Camera off"))
		button.doAction()
		focus.setFocus()

	# Натиснути кнопку "Вкласти медіа"
	@script(description=_("Press \"Attach file\" button"), gesture="kb:control+shift+A")
	def script_add_files(self, gesture):
		button = next((item for item in self.get_elements() if controlTypes.State.FOCUSABLE in item.states and item.UIAAutomationId == "AttachButton"), None)
		if button: button.doAction()
		else: message(_("Button not found"))

		# Натиснути кнопку "Нова розмова"
	
	# Натиснути кнопку "Більше опцій"
	@script(description=_("Press \"More Options\" button"), gesture="kb:ALT+O")
	def script_showMoreOptions(self, gesture):
		button = next((item for item in self.get_elements() if item.role == controlTypes.Role.BUTTON and item.UIAAutomationId == "SettingsButton"), None)
		if button: button.doAction()
		else: message(_("Button not found"))

	# Функція запису і надсилання голосового повідомлення
	@script(description=_("Record and send a voice message"), gesture="kb:control+R")
	def script_recordingVoiceMessage(self, gesture):
		button = next((item for item in self.get_elements() if item.role == controlTypes.Role.BUTTON and controlTypes.State.FOCUSABLE in item.states and item.UIAAutomationId in ("RightButton", "PttSendButton")), None)
		if not button: return
		if button.UIAAutomationId == "RightButton":
			if button.firstChild.name == "\ue724":
				# Якщо поле вводу не порожнє
				message(_("Recording a voice message will not be available until the edit field is empty"))
				return
			if config.conf["WhatsAppPlus"]['playSoundWhenRecordingVoiceMessage']:
				playWaveFile(baseDir+"wa_ptt_start_record.wav")
			self.is_skip_name = 2
			button.doAction()
		elif button.UIAAutomationId == "PttSendButton":
			self.is_skip_name = 2
			button.doAction()
			if config.conf["WhatsAppPlus"]['playSoundWhenRecordingVoiceMessage']:
				playWaveFile(baseDir+"wa_ptt_sent.wav")

	# Фунція скасовування запису голосового повідомлення
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
	
	# Фунція призупиненя запису голосового повідомлення
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
		self.activate_option_for_menu(icon_from_context_menu["переслати повідомлення"])
	@script(description=_("React to message"), gesture="kb:ALT+Q")
	def script_set_reaction(self, gesture):
		self.activate_option_for_menu(icon_from_context_menu["встановити реакцію"])
	@script(description=_("Delete a message or chat"), gesture="kb:ALT+delete")
	def script_deletion(self, gesture):
		self.activate_option_for_menu(icon_from_context_menu["видалити"])
	@script(description=_("Reply to message"), gesture="kb:ALT+R")
	def script_reply_to_message(self, gesture):
		self.activate_option_for_menu(icon_from_context_menu["відповісти на повідомлення"])
	@script(description=_("Mark a chat as read"), gesture="kb:ALT+shift+R")
	def script_read_chat(self, gesture):
		self.activate_option_for_menu((icon_from_context_menu["помітити як прочитаний"], icon_from_context_menu["позначити як непрочитаний"]))
	@script(description=_("Star message"), gesture="kb:ALT+S")
	def script_Star_message(self, gesture):
		self.activate_option_for_menu((icon_from_context_menu["добавити в обрані"], icon_from_context_menu["видалити з обраних"]))
	@script(description=_("Save file as..."))
	def script_save_file(self, gesture):
		self.activate_option_for_menu(icon_from_context_menu["зберегти як"])
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

	# Перемикання режиму видалення номеру телефону в іменах контактів	
	@script(description=_("Toggles the mode that removes the reading of the user number when reading messages that are not in the contact list"), gesture="kb:control+shift+E")
	def script_save_as(self, gesture):
		config.conf["WhatsAppPlus"]["displayPhoneNumberInUsername"] = not config.conf["WhatsAppPlus"]["displayPhoneNumberInUsername"]
		if config.conf["WhatsAppPlus"]["displayPhoneNumberInUsername"]: message(_("User numbers will be read"))
		else: message(_("User numbers will not be read"))

	@script(description=_("Enable automatic reading of new messages in the current chat"), gesture="kb:ALT+L")
	def script_toggle_live_chat(self, gesture):
		if config.conf["WhatsAppPlus"]["automaticReadingOfNewMessages"]:
			config.conf["WhatsAppPlus"]["automaticReadingOfNewMessages"] = False
			Chat_update.toggle(self, False)
			message(_("Automatic reading of new messages is disabled"))
		elif not Chat_update.active and not config.conf["WhatsAppPlus"]["automaticReadingOfNewMessages"]:
			Chat_update.toggle(self, True)
			message(_("Automatic reading of new messages is enabled until the NVDA is restarted"))
		elif Chat_update.active and not config.conf["WhatsAppPlus"]["automaticReadingOfNewMessages"]:
			config.conf["WhatsAppPlus"]["automaticReadingOfNewMessages"] = True
			message(_("Automatic reading of messages is enabled"))

	# Обробляємо повідомлення яке потрапило в фокус
	def action_message_focus(self, obj):
		reactions = ""
		answer = False
		duration = False
		time_element = False
		# Тут зберігаємо текст відповіді, якщо повідомлення було написано у відповідь
		text = False
		for item in obj.children:
			if item.UIAAutomationId == "Text": text = item
			elif item.UIAAutomationId == "TextBlock" and item.next and item.next.UIAAutomationId in ("ReadMore", "Scrubber"):
				time_element = item.name
				item = item.previous
				try:
					if text and obj.firstChild.UIAAutomationId in ("", "NameTextBlock"):
						# Тут зберігаємо ім'я користувача, яке потрібно вирізати з повідомлення
						name = obj.children[0]
						# Тут зберігаємо ім'я користувача, яке потрібно буде дописати в кінці повідомлення
						new_name = text.previous
						# У випадку, коли користувач з номером телефону відповідає на моє повідомлення посиланням
						if new_name.previous and new_name.previous.UIAAutomationId == "PushNameTextBlock": name =new_name
						answer = (name.name, new_name.name, text.name.strip())
				except: pass
			elif item.UIAAutomationId == 'ReactionBubble':
				reactions = item.name
			elif item.UIAAutomationId == "Duration": duration = item.name
			elif item.UIAAutomationId == "TitleTextBlock"and " http" in obj.name:
				# Якщо повідомлення містить посилання, тоді намагаємось відобразити опис даного посилання
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

		# Видаляємо номери телефону з імен користувачів
		if not config.conf["WhatsAppPlus"]["displayPhoneNumberInUsername"]: obj.name = sub(reg_for_delete_phon_number, '', obj.name)
	
	
	__gestures = {
		"kb:space": "action_space",
		"kb:ALT+leftArrow": "back",
	}


	def event_gainFocus(self, obj, nextHandler):
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
			elif obj.UIAAutomationId == "ChatsListItem":
				speech.cancelSpeech()
				self.last_focus_chat_element = obj
		elif obj.role == controlTypes.Role.EDITABLETEXT and obj.UIAAutomationId == "TextBox":
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


	# Обробляємо ініціалізацію елементів
	# def chooseNVDAObjectOverlayClasses(self, obj, clsList):
	def event_NVDAObject_init(self,obj):
		try:
			if obj.role == controlTypes.Role.LISTITEM:
				if obj.name in ('WhatsApp.CallParticipantVm', 'WhatsApp.SelfStreamVm', 'WhatsApp.RecipientItem', 'WhatsApp.ReceiptViewModel'):
					obj.name = ", ".join([m.name for m in obj.children])
				elif obj.name == 'WhatsApp.Design.LightBoxExtendedTextItemVm':
					obj.name = obj.firstChild.name
				elif obj.name == 'WhatsApp.Design.ThemeData':
					obj.name = obj.children[1].name
				elif controlTypes.State.SELECTED in obj.states and obj.parent.UIAAutomationId in ("EmojiList", "MentionsList"):
					# Озвучуємо ім'я вибраного користувача в списку з підказками, при ведені символа @
					message(obj.name)
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
			elif obj.role == controlTypes.Role.TOGGLEBUTTON:
				if obj.UIAAutomationId in ("WhenWAClosedSwitch", "NewMessagesNotificationSwitch"): obj.name = obj.previous.name
			elif obj.role == controlTypes.Role.GROUPING:
				# if obj.name in ('WhatsApp.WaCollections.KeyedObservableCollection`2[WhatsApp.GroupItem,WhatsApp.RecipientItem]'):
					# obj.name = obj.children[0].name
				if obj.name in ('WhatsApp.ViewModels.EmojiPickerCategoryViewModel', 'WhatsApp.Pages.Recipients.RecipientGroupingVm`1[WhatsApp.Pages.Recipients.NewChatVm+IItem]', 'WhatsApp.Pages.Recipients.RecipientGroupingVm`1[WhatsApp.Pages.Recipients.ForwardMessageVm+IItem]', 'WhatsApp.Pages.Recipients.RecipientGroupingVm`1[WhatsApp.AddCallParticipantsVm+IItem]', 'WhatsApp.Pages.Recipients.UserRecipientItemVm'):
					obj.name = obj.firstChild.name
			elif obj.role == controlTypes.Role.SLIDER:
				if obj.UIAAutomationId == "Scrubber" and obj.value != "0": self.rewind_slider = obj
			elif obj.role == controlTypes.Role.PROGRESSBAR:
				message(obj.value)
				message(obj.name)
		except: pass

	def _event_nameChange(self, obj, nextHandler):
		message(obj.name)
		if obj.role == controlTypes.Role.PROGRESSBAR:
			message(str(obj.value))
		nextHandler()

	def event_valueChange(self, obj, nextHandler):
		# message(obj.value)
		# message(obj.name)
		if obj.UIAAutomationId == "Scrubber": self.rewind_slider = obj
		nextHandler()