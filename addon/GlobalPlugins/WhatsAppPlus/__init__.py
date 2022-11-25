# -*- coding: utf-8 -*-
import globalPluginHandler
import addonHandler
from scriptHandler import script
import config
import gui
from gui import SettingsPanel, guiHelper, nvdaControls
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
		if config.conf["WhatsAppPlus"]["isAutomaticallyCheckForUpdates"]:
			threading.Thread(target=onCheckForUpdates, args=(False, True,)).start()

	@script(description=_("Open WhatsAppPlus settings window"), gesture="kb:NVDA+control+W")
	def script_open_settings_dialog(self, gesture, arg = False):
		wx.CallAfter(gui.mainFrame._popupSettingsDialog, gui.settingsDialogs.NVDASettingsDialog, WhatsAppPlusSettings)

class WhatsAppPlusSettings(gui.SettingsPanel):
	title = "WhatsAppPlus"
	def makeSettings(self, settingsSizer):
		settingsSizerHelper = gui.guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
		# Field for setting the function of moving focus to unread messages
		self.phrases_of_unread_messages = settingsSizerHelper.addLabeledControl(_('In this field, separate by commas, write all the matching phrases of the "Unread messages" element in your language. You need to write phrases without a number.'), wx.TextCtrl)
		self.phrases_of_unread_messages.Value = getConfig("phrasesOfUnreadMessages")
		# Turn on sounds when recording voice messages
		self.is_play_sound_when_recording_voice_message = settingsSizerHelper.addItem(wx.CheckBox(self, label=_("Play sounds when starting, pausing and sending a voice message")))
		self.is_play_sound_when_recording_voice_message.SetValue(getConfig("playSoundWhenRecordingVoiceMessage"))
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
		phrases_of_unread_messages = self.phrases_of_unread_messages.Value.split(",")
		phrases_of_unread_messages = [item.lower().strip() for item in phrases_of_unread_messages]
		self.phrases_of_unread_messages.Value = ",".join(phrases_of_unread_messages)
		setConfig("phrasesOfUnreadMessages", self.phrases_of_unread_messages.Value)
		setConfig("isAutomaticallyCheckForUpdates", self.is_automatically_check_for_updates.IsChecked())
		setConfig("playSoundWhenRecordingVoiceMessage", self.is_play_sound_when_recording_voice_message.IsChecked())

	def onPanelActivated(self):
		self.originalProfileName = config.conf.profiles[-1].name
		config.conf.profiles[-1].name = None
		self.Show()

	def onPanelDeactivated(self):
		config.conf.profiles[-1].name = self.originalProfileName
		self.Hide()
