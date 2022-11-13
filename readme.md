# WhatsAppPlus

* Author: Kostya Gladkiy (Ukrain)
* [Telegram channel](https://t.me/unigramPlus)

##Information about the opportunity to donate to the developer:

If you have the desire, and most importantly the opportyunity, to support the developer of this add-on, you can do so using the following details:

* PayPal: gladkiy.kostya@gmail.com.
* Ukrainian donation system: https://unigramplus.diaka.ua/donate.
* Card number: 5169360009004502 (Gladkiy Constantine).

Added a large number of keyboard shortcuts for productive and comfortable work in the program, which can be found below.

### General add-on features

* Now the message input field will change its name when we reply to a message.
* Added labels for some program elements that are read by screen readers.

## Hotkey list:

* ALT+1 - Move focus to chat list.
* ALT+2 - Move focus to the last message in an open chat.
* ALT+D - Move the focus to the edit field. If the focus is already in the edit field, then after pressing the hotkey, it will move to where it was before.
* ALT+T - Announce the name and status of an open chat.
* ALT+shift+C - Make a voice call to a group or contact, or join an ongoing voice call in a group.
* ALT+shift+V - Make a video call to a contact or group.
* ALT+Y - Accept call.
* ALT+N - Press "Decline call" button  if there is an incoming call, "or call" button if a call is in progress.
* ALT+A - Turn the camera microphone and off.l
* ALT+V - Turn the camera on and off.l
* ALT+O - Press "More Options" button.
* control+R - Record and send a voice message.
* control+D - Discard voice message.
* control+shift+D - Pause/resume voice message recording.
* ALT+delete - Delete a message or chat.
* control+shift+P - Open current chat profile.
* control+shift+E - Toggles the mode that removes the reading of the user number when reading messages that are not in the contact list.
* ALT+Q - React to message.
* ALT+S - Star message.
* ALT+F - Forward message.
* ALT+R - Reply to message.
* ALT+shift+R - Mark a chat as read.
* control+C - Copy the message if it contains text.
* ALT+C - Show message text in popup window.
* NVDA+control+W - Open WhatsAppPlus settings window.
* ALT+3 - Move focus to "unread messages" label.
* control+shift+A - Press "Attach file" button.
* ALT+L: Enable automatic reading of new messages in the current chat.
* control+S: Increase/decrease the playback speed of voice messages.
* ALT+P: Play/pause the voice message currently playing.

## History of changes

### Version 1.6.0

* Added ability to quickly reply to group members. To enter a message, it is enough to write the symbol "@" in the message entry field, use the up and down arrows to select who you want to reply to, and then press the Enter key.
* Added ability to quickly insert emoticons. To do this, you must write a colon and the name of the emoticon you want to find in the message input field. Later, use the left and right arrow keys to find the desired emoticon and use the Enter key to insert it into the message input field.
* In the WhatsAppPlus settings, an option has been added to enable the playback of sounds when recording, pausing and sending voice messages.
* Changed the keyboard shortcut for opening the profile of the current conversation to Control+Shift+P.
* Added Nepali localization.
* Fixed several bugs, including an issue where automatic reading of new messages in an open conversation was not working for some users.

### Version 1.5.0

*Added a keyboard shortcut to change the speed of the voice message being played. The default gesture is ctrl+s. The gesture will only work when a voice message is playing in an open chat.
* Added a keyboard shortcut to pause a voice message that is playing. The default gesture is alt+p. The function will only work when a voice message is playing in an open chat.
* Now the announcement of a new message in an open chat can be enabled not only until NVDA is restarted, but also forever.

### Version 1.4.0

* Adapted to the latest version of WhatsApp.
* The function of automatic announcements of new messages in the chat has been added. By default, this function is activated by pressing ALT+L. The feature remains active only until NVDA is restarted. There may be stability issues if too many new messages.
* Added French localization.

### Version 1.3.0

* The description of the links attached to the message will now be read.
* Now the duration of voice messages will be announced.
* You can now open links attached to messages with the spacebar
* Added labels for some interface elements
* Adapted to the latest version of WhatsApp so that all functions work properly.
* Fixed some bugs

### Version 1.2.0

* Now, when you focus on a message written in reply to another message, the text of that message will be spoken first and then the text of the message to which it was sent.
* The name and type of files sent in the conversation will now be spoken.
* ALT+1 now works even when the chat archive or the selected messages section is open.
* ALT + left arrow helps to close the chat archive or the selected messages list if they are open.
* Now, pressing control+D, in addition to cancelling voice messages, also cancels the reply to the message.
* Information about the inability to record a voice message will now be reported when the message input field is not empty. This will fix a problem where pressing control+R would send a text message instead of starting a voice message recording.
* Labeled some items that didn't have labels already.

### Version 1.1.0

* Added keyboard shortcut to navigate to unread messages. Since this feature is language dependent, this feature can be configured in the WhatsAppPlus settings.
* Added a keyboard shortcut for pressing the "New Chat" button.
* Added a keyboard shortcut for pressing the "Attach file" button.
* Now, when recording a voice message, the synthesizer will not announce the names of the recording control buttons.
* Added Arabic, Italian, Romanian, Serbian, Croatian, Spanish and Turkish localizations.
* Added labels for some elements that didn't have screen reader labels.
* Now information about reactions to a message will be announced when focusing on a message.
* Now when playing your own voice messages with the spacebar, a pop-up window will not appear.
* Fixed minor bugs.
