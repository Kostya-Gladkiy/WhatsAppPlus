# -*- coding: utf-8 -*-
import globalPluginHandler
import addonHandler
from scriptHandler import script
import config
import gui
from gui import SettingsPanel, guiHelper, nvdaControls
import wx
import core
import globalVars
import os
addonHandler.initTranslation()
import languageHandler
import queueHandler
import threading, time, queue, random
from appModules.whatsapp import SPEC


lang = languageHandler.getLanguage().split("_")[0]


def getConfig(key):
	return config.conf["WhatsAppPlus"][key]

def setConfig(key, value):
	config.conf["WhatsAppPlus"][key] = value
	return
	try:
		config.conf.profiles[0]["WhatsAppPlus"][key] = value
	except:
		config.conf["WhatsAppPlus"][key] = value

	def window_close(self, event):
		self.Close()


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	scriptCategory = "WhatsAppPlus"
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		config.conf.spec['WhatsAppPlus'] = SPEC
		gui.settingsDialogs.NVDASettingsDialog.categoryClasses.append(WhatsAppPlusSettings)

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
		setConfig("playSoundWhenRecordingVoiceMessage", self.is_play_sound_when_recording_voice_message.IsChecked())

	def onPanelActivated(self):
		self.originalProfileName = config.conf.profiles[-1].name
		config.conf.profiles[-1].name = None
		self.Show()

	def onPanelDeactivated(self):
		config.conf.profiles[-1].name = self.originalProfileName
		self.Hide()
