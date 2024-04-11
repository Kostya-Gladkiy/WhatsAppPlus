# WhatsAppPlus #

* Author: Kostya Gladkiy (Ukrain)
* Download [stable version][1] (Compatible with NVDA 2021.2 to 2023.1)
* [Telegram channel][2]

## About ##

This add-on makes it easy to use the UWP version of the WhatsApp app, allowing users to easily interact with chats, messages, context menu items, and more.

### General features ###

* When replying to a message, the edit field will change the title.
* Added accessibility labels for some WhatsApp elements.
* A large number of keyboard shortcuts have been added to work productively and comfortably in WhatsApp, which can be found below.

## Keyboard shortcuts: ##

* ALT+1: Move focus to chat list.
* ALT+2: Move focus to the last message in an open chat.
* ALT+D: Move the focus to the edit field. If the focus is already in the edit field, then after pressing the hotkey, it will move to where it was before.
* ALT+T: Announce the name and status of an open chat.
* ALT+shift+C: Make a voice call to a group or contact.
* ALT+shift+V: Make a video call to a contact or group.
* NVDA+ALT+Y: Accept call.
* NVDA+ALT+N: Decline an incoming call or leave the current call.
* ALT+A: Turn the microphone on/off.
* ALT+V: Turn video on/off.
* ALT+O: Press more options button.
* control+R: Record and send a voice message.
* control+D: Discard reply to a message or currently recorded voice message.
* control+shift+D: Pause/resume voice message recording.
* ALT+delete: Delete a message or chat.
* control+shift+P: Open current chat profile.
* control+shift+E: Toggles the feature that removes the reading of the user number in messages from users whose number is not saved in the contact list.
* ALT+S: Star message.
* ALT+F: Forward message.
* ALT+R: Reply to message.
* ALT+shift+R: Mark a chat as read.
* control+C: Copy the message if it contains text.
* ALT+C: Show message text in popup window.
* NVDA+control+W: Open WhatsAppPlus settings window.
* ALT+3: Move focus to "unread messages" label.
* control+shift+A: Press the attach file button.
* ALT+L: Enable automatic reading of new messages in the current chat.
* control+S: Increase/decrease the playback speed of voice messages.
* ALT+P: Play/pause a voice message that is playing.
* ALT+U: announce the current value of a progress bar. If pressed twice, turns on/off the automatic announcement of progress bars.
* control+space: Switch to selection mode.
* ALT+backspace: Edit message.

### Information about the opportunity to donate to the developer: ###

If you have a desire, and most importantly, the opportunity to support the developer of this add-on, you can do it using the following details:

* PayPal: gladkiy.kostya@gmail.com.
* [Ukrainian donation system][3]
* Card number: 5169360009004502 (Gladkiy Constantine).

## Changelog ##

### Version 2.1.0 ###

* Fixed the problem with reading user status.
* Fixed an issue where it was not possible to answer a call and reject a call with a keyboard shortcut. Note that the keyboard shortcuts for answering and rejecting a call have been changed to NVDA+ALT+Y and NVDA+ALT+N.
* Fixed incorrect operation of the function that reads new messages in open chat.
* Fixed an issue where the phone number was read instead of your name in messages that you sent.
* Fixed an issue with sending voice messages using control+R.
* Added compatibility with NVDA 2024.1.

### Version 2.0.0 ###

* Added keyboard shortcut for editing messages. By default, this function is assigned to the ALT+backspace combination.
* Focusing on a message containing a file will now speak the name, type, and size of the file.
* Now the function of automatically reading new messages in open chat works correctly. Note though that for correct operation you need to specify your phone number and your name in the WhatsAppPlus settings.that for correct operation you need to specify your phone number in the WhatsAppPlus settings.
* Now the function of automatic reading of activity in open chats will work more stably.
* ALT+D now works correctly.
* Fixed conflict of some functions with "BluetoothAudio" add-on.

### Version 1.9.0 ###

* Added a keyboard shortcut that opens a list of all WhatsAppPlus keyboard shortcuts. By default, this function is assigned to ALT+H gesture.
* Fixed a bug where ALT+2 and ALT+3 gestures didn't work.
* Fixed a bug where it was impossible to activate some functions from the context menu using gestures.
* Fixed an issue where changing voice message playback speed and pausing voice message playback did not always work.
* Fixed a bug where in chats when focusing on your sent messages, instead of the word "you", the screen reader announced a personal number. To avoid this, you need to specify the phone number in the WhatsAppPlus settings and after that the add-on will not report it on your messages.
* Fixed an issue where WhatsAppPlus prompted to update on secure screens. To prevent this from happening again, you need to click on the "Use currently saved settings during sign-in and on secure screens (requires administrator privileges)" button in the NVDA general settings.
* The gesture to accept a call has been changed to ALT+shift+Y, and the gesture to decline a call has been changed to ALT+shift+N. This is to ensure that these gestures do not conflict with UnigramPlus gestures.
* Microphone and camera on/off gestures during a call now work correctly.
* Removed gesture to set reaction to messages, since in the latest versions of WhatsApp, reactions are available directly from the context menu.

### Version 1.8.0 ###

* The add-on has been tested to ensure compatibility with NVDA-2023.
* Added a keyboard shortcut for selecting messages. To enter selection mode, press Ctrl+Space, and then use Space to select the next message.
* A new function has been added to automatically announce activity in an open chat. By default, this feature is enabled by double-pressing the ALT+T gesture. This helps users stay up to date with new messages and other chat activities.
* The automatic reading of new chat messages has been significantly redesigned to be more stable. This ensures that users are alerted to new messages accurately and reliably.
* Added labels for some unlabeled buttons.

### Version 1.7.0 ###

* Added a function that automatically announces the progress bar if the focus is on a message.
* Added a keyboard shortcut to report the value of the progress bar when the focus is on a message. By default, the ALT+U gesture is assigned to this feature. If the gesture is pressed twice, the automatic announcement of the progress bar values will be enabled.
* Fixed an issue where focus could not be moved to the chat list.
* Added labels to some elements.

### Version 1.6.0 ###

* Added ability to quickly reply to group members. To enter a message, it is enough to write the symbol "@" in the message entry field, use the up and down arrows to select who you want to reply to, and then press the Enter key.
* Added ability to quickly insert emoticons. To do this, you must write a colon and the name of the emoticon you want to find in the message input field. Later, use the left and right arrow keys to find the desired emoticon and use the Enter key to insert it into the message input field.
* In the WhatsAppPlus settings, an option has been added to enable the playback of sounds when recording, pausing and sending voice messages.
* Changed the keyboard shortcut for opening the profile of the current conversation to Control+Shift+P.
* Added Nepali localization.
* Fixed several bugs, including an issue where automatic reading of new messages in an open conversation was not working for some users.

### Version 1.5.0 ###

* Added a keyboard shortcut to change the speed of the voice message being played. The default gesture is ctrl+s. The gesture will only work when a voice message is playing in an open chat.
* Added a keyboard shortcut to pause a voice message that is playing. The default gesture is alt+p. The function will only work when a voice message is playing in an open chat.
* Now the announcement of a new message in an open chat can be enabled not only until NVDA is restarted, but also forever.

### Version 1.4.0 ###

* Adapted to the latest version of WhatsApp.
* Added automatic reading of new messages in open chat. By default, this feature is activated by pressing ALT+L. The feature remains active only until NVDA is restarted. May have stability issues if there are too many new messages.
* Added French localization.

### Version 1.3.0 ###

* The description of the links attached to the message will now be read.
* Now the duration of voice messages will be announced.
* You can now open links attached to messages with the spacebar
* Added labels for some interface elements
* Adapted to the latest version of WhatsApp so that all functions work properly.
* Fixed some bugs

### Version 1.2.0 ###

* Now, when you focus on a message written in reply to another message, the text of that message will be spoken first and then the text of the message to which it was sent.
* The name and type of files sent in the conversation will now be spoken.
* ALT+1 now works even when the chat archive or the selected messages section is open.
* ALT + left arrow helps to close the chat archive or the selected messages list if they are open.
* Now, pressing control+D, in addition to cancelling voice messages, also cancels the reply to the message.
* Information about the impossibility of recording a voice message will now be reported when the message input field is not empty. This will fix an issue where pressing Ctrl+R would send a text message instead of starting to record a voice message.
* Added labels for unlabeled elements.

### Version 1.1.0 ###

* Added keyboard shortcut to navigate to unread messages. Since this feature is language dependent, this feature can be configured in the WhatsAppPlus settings.
* Added keyboard shortcut for pressing the new chat button.
* Added keyboard shortcut for pressing the attach file button.
* NVDA will no longer announce the recording control buttons when recording a voice message.
* Added Arabic, Italian, Romanian, Serbian, Croatian, Spanish and Turkish localizations.
* Added labels for some unlabeled elements.
* Now information about the reaction to the message will be announced when focusing on the message.
* Now, when playing your own voice messages using the spacebar, a pop-up window will not appear.
* Fixed minor bugs.

[1]: https://www.nvaccess.org/addonStore/legacy?file=whatsAppPlus

[2]: https://t.me/unigramPlus

[3]: https://unigramplus.diaka.ua/donate
