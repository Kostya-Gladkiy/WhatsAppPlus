# -*- coding: utf-8 -*-
import api
import IAccessibleHandler
import globalPluginHandler
import addonHandler
from scriptHandler import script
import config
import gui
from gui import guiHelper, nvdaControls
from gui.settingsDialogs import SettingsPanel
import wx
import urllib.request
import core
import globalVars
import os
addonHandler.initTranslation()
import languageHandler
import queueHandler
import threading, time, queue, random
from appModules.whatsapp import SPEC
from appModules.whatsapp import AppModule


lang = languageHandler.getLanguage().split("_")[0]
path_to_server = "http://46.254.107.124/addons/whatsappplus/"


def getConfig(key):
    return config.conf["WhatsAppPlus"][key]

def setConfig(key, value):
	config.conf["WhatsAppPlus"][key] = value
	return
	try:
		config.conf.profiles[0]["WhatsAppPlus"][key] = value
	except:
		config.conf["WhatsAppPlus"][key] = value

def no_updates_dialog():
	res = gui.messageBox(
		_("No updates available"),
		_("WhatsAppPlus update"),
		wx.OK | wx.ICON_INFORMATION)

def onCheckForUpdates(event = False, is_start = False):
	import versionInfo
	NVDAVersion = f"{versionInfo.version_year}.{versionInfo.version_major}.{versionInfo.version_minor}"
	NVDAVersion = int(NVDAVersion.replace(".", ""))
	fp = os.path.join(globalVars.appArgs.configPath, "whatsappplus.nvda-addon")
	addon_version = addonHandler.getCodeAddon().manifest["version"]
	addon_version = int(addon_version.replace(".", ""))
	try: response = urllib.request.urlopen(path_to_server+"version.txt").read().decode('utf-8')
	except:
		if not is_start: wx.CallAfter(no_updates_dialog)
		return
	response = str(response)
	str_last_version = response.split("\n")[0]
	last_version = int(str_last_version.replace(".", ""))
	minimum_version = response.split("\n")[1]
	minimum_version = int(minimum_version.replace(".", ""))
	url = response.split("\n")[-1]
	if last_version > addon_version and NVDAVersion >= minimum_version:
		wx.CallAfter(window_for_update, None, str_last_version, url)
	elif not is_start: wx.CallAfter(no_updates_dialog)

class window_for_update(wx.Frame):
	def __init__(self, parent, str_last_version, url):
		title = _("WhatsAppPlus update")
		text = _("A new version of the add-on is available. Do you want to update WhatsAppPlus to version %version?").replace("%version", str_last_version)
		no_resize = wx.DEFAULT_FRAME_STYLE & ~ (wx.RESIZE_BORDER | wx.MAXIMIZE_BOX)
		# wx.Frame.__init__(self, parent, title = title, size = (640, 360), style=no_resize)
		wx.Frame.__init__(self, parent, title = title, size = (640, 360))
		self.url = str(url)
		self.str_last_version = str_last_version
		self.Centre()
		panel = wx.Panel(self)
		self.text = wx.TextCtrl(panel, -1, text, style = wx.TE_MULTILINE | wx.TE_READONLY)
		self.text.SetValue(text)
		self.text.SetFocus()
		self.button_ok = wx.Button(panel, label=_("Yes, update"))
		self.button_close= wx.Button(panel, label=_("No, not now"))
		self.button_ok.Bind(wx.EVT_BUTTON,self.download_update)
		self.button_close.Bind(wx.EVT_BUTTON,self.window_close)
		sizer = wx.BoxSizer(wx.VERTICAL)
		buttons_sizer = wx.BoxSizer(wx.HORIZONTAL)
		buttons_sizer.Add(self.button_ok, 0, wx.LEFT | wx.RIGHT, 5)
		buttons_sizer.Add(self.button_close, 0, wx.LEFT | wx.RIGHT, 5)
		sizer.Add(self.text, 1, wx.ALL | wx.EXPAND, 5)
		sizer.Add(buttons_sizer, flag = wx.ALL | wx.ALIGN_RIGHT, border=5)
		panel.SetSizer(sizer)
		self.Raise()
		self.Show(True)
		self.get_documentation()

	def download_update(self, event):
		self.text.SetValue(_("Download in progress"))
		self.text.SetFocus()
		try: response_addon = urllib.request.urlopen(self.url).read()
		except:
			no_updates_dialog()
			self.Close()
			return
		fp = os.path.join(globalVars.appArgs.configPath, "whatsappplus.nvda-addon")
		with open(fp, 'wb') as addon:
			addon.write(response_addon)
		self.setup_update(fp)
		self.button_ok.Disable()
		self.button_close.Disable()

	def window_close(self, event):
		self.Close()
	
	def get_documentation(self):
		doc = False
		url = path_to_server+"documentation/"+self.str_last_version+"/"+lang+".txt"
		try: doc = urllib.request.urlopen(url).read().decode('utf-8')
		except: pass
		try:
			url = path_to_server+"documentation/"+self.str_last_version+"/en.txt"
			if not doc: doc = urllib.request.urlopen(url).read().decode('utf-8')
		except: pass
		if doc: text = "\n"+_("Changes in this version:")+"\n"+str(doc)
		else: text = "\n"+_(_("No update information"))
		self.text.SetValue(self.text.GetValue()+text)

	def setup_update(self, fp):
		curAddons = addonHandler.getAvailableAddons()
		bundle = addonHandler.AddonBundle(fp)
		bundleName = bundle.manifest['name']
		prevAddon = next((addon for addon in curAddons if not addon.isPendingRemove and bundleName == addon.manifest['name']), None)
		if prevAddon: prevAddon.requestRemove()
		addonHandler.installAddonBundle(bundle)
		core.restart()


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	scriptCategory = "WhatsAppPlus"
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		config.conf.spec['WhatsAppPlus'] = SPEC
		gui.settingsDialogs.NVDASettingsDialog.categoryClasses.append(WhatsAppPlusSettings)
		# Check if the user folder contains a temporary add-on file, if so, then delete it
		fp = os.path.join(globalVars.appArgs.configPath, "whatsappplus.nvda-addon")
		if os.path.exists(fp): os.remove(fp)
		# Checking for updates
		obj = api.getFocusObject()
		if config.conf["WhatsAppPlus"]["isAutomaticallyCheckForUpdates"] and not globalVars.appArgs.secure:
			threading.Thread(target=onCheckForUpdates, args=(False, True,)).start()

	# Call answer
	@script(description=_("Accept call"), gesture="kb:NVDA+ALT+Y")
	def script_answeringCall(self, gesture):
		gesture.send()
		desctop = api.getDesktopObject()
		notification = next((item.firstChild.firstChild for item in desctop.children if item.firstChild and hasattr(item.firstChild, "UIAAutomationId") and item.firstChild.UIAAutomationId == "ToastCenterScrollViewer"), False)
		if not notification:
			return
		button = next((item for item in notification.children if item.UIAAutomationId == "VerbButton"), None)
		if button: button.doAction()

	# End or decline call
	@script(description=_("Press \"Decline call\" button  if there is an incoming call or \"End call\" button if a call is in progress"), gesture="kb:NVDA+ALT+N")
	def script_callCancellation(self, gesture):
		desctop = api.getDesktopObject()
		notification = next((item.firstChild.firstChild for item in desctop.children if item.firstChild and hasattr(item.firstChild, "UIAAutomationId") and item.firstChild.UIAAutomationId == "ToastCenterScrollViewer"), False)
		if not notification: return
		button = next((item.next for item in notification.children if item.UIAAutomationId == "VerbButton"), None)
		if button:
			button.doAction()
			return
		AppModule.script_callCancellation(AppModule, gesture)


	@script(description=_("Open WhatsAppPlus settings window"), gesture="kb:NVDA+control+W")
	def script_open_settings_dialog(self, gesture, arg = False):
		wx.CallAfter(gui.mainFrame._popupSettingsDialog, gui.settingsDialogs.NVDASettingsDialog, WhatsAppPlusSettings)

class WhatsAppPlusSettings(gui.SettingsPanel):
	title = "WhatsAppPlus"
	def makeSettings(self, settingsSizer):
		settingsSizerHelper = gui.guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
		# A field for entering a user name so that the application can replace the phone number with the phrase "You" in messages
		self.user_name = settingsSizerHelper.addLabeledControl(_("Enter the name that you have provided in your WhatsApp account. This is so that WhatsAppPlus can distinguish your messages from other messages."), wx.TextCtrl)
		self.user_name.Value = getConfig("user_name")
		# A field for entering a phone number so that the application can replace the phone number with the phrase "You" in messages
		self.number_phone = settingsSizerHelper.addLabeledControl(_("Enter a phone number. This is to prevent the app from displaying your phone number on messages sent by you."), wx.TextCtrl)
		self.number_phone.Value = getConfig("number_phone")
		# Field for setting the function of moving focus to unread messages
		self.phrases_of_unread_messages = settingsSizerHelper.addLabeledControl(_('In this field, separate by commas, write all the matching phrases of the "Unread messages" element in your language. You need to write phrases without a number.'), wx.TextCtrl)
		self.phrases_of_unread_messages.Value = getConfig("phrasesOfUnreadMessages")
		# Turn on sounds when recording voice messages
		self.is_play_sound_when_recording_voice_message = settingsSizerHelper.addItem(wx.CheckBox(self, label=_("Play sounds when starting, pausing and sending a voice message")))
		self.is_play_sound_when_recording_voice_message.SetValue(getConfig("playSoundWhenRecordingVoiceMessage"))
		# Automatically report progress indicators
		self.automatically_report_progress_indicators = settingsSizerHelper.addItem(wx.CheckBox(
		    self, label=_("Automatically report progress bar updates when focus is on a message")))
		self.automatically_report_progress_indicators.SetValue(
		    getConfig("automatically_report_progress_indicators"))
		# Checking for Updates on NVDA Startup
		self.is_automatically_check_for_updates = settingsSizerHelper.addItem(wx.CheckBox(self, label=_("Check for WhatsAppPlus updates on NVDA startup")))
		self.is_automatically_check_for_updates.SetValue(getConfig("isAutomaticallyCheckForUpdates"))
		# Button to check for updates
		self.checkForUpdates = settingsSizerHelper.addItem(wx.Button(self, label=_("Check for &updates")))
		self.checkForUpdates.Bind(wx.EVT_BUTTON, onCheckForUpdates)

	def get_key(self, d, value):
		for k, v in d.items():
			if v == value: return k

	def onSave(self):
		setConfig("user_name", self.user_name.Value)
		setConfig("number_phone", self.number_phone.Value)
		phrases_of_unread_messages = self.phrases_of_unread_messages.Value.split(",")
		phrases_of_unread_messages = [item.lower().strip() for item in phrases_of_unread_messages]
		self.phrases_of_unread_messages.Value = ",".join(phrases_of_unread_messages)
		setConfig("phrasesOfUnreadMessages", self.phrases_of_unread_messages.Value)
		setConfig("automatically_report_progress_indicators", self.automatically_report_progress_indicators.Value)
		setConfig("isAutomaticallyCheckForUpdates", self.is_automatically_check_for_updates.IsChecked())
		setConfig("playSoundWhenRecordingVoiceMessage", self.is_play_sound_when_recording_voice_message.IsChecked())

	def onPanelActivated(self):
		self.originalProfileName = config.conf.profiles[-1].name
		config.conf.profiles[-1].name = None
		self.Show()

	def onPanelDeactivated(self):
		config.conf.profiles[-1].name = self.originalProfileName
		self.Hide()
