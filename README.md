# Echo Linguistics
Using Alexa's Speech Synthesis Markup Language Support to Extend Amazon Echo Voice Capabilities


- Change the file save name to actually indicate the contents of the file in testFunction/lambda_function.py

### How does this work?

The Alexa Skill Kit offers 2 ways for developers to play audio on Amazon Echo devices.

- Audio Streaming (Spotify, Amazon Music, etc.)

- Speech Synthesis Markup Support (Buzzer in games, timer going off, etc.)




Amazon describes SSML as the following:
> SSML is a markup language that provides a standard way to mark up text for the generation of synthetic speech


With SSML, developers can tell Alexa to enunciate words a certain way (Tomato vs. Tomoto).  SSML can also be used to play audio files on the echo, but it differs from regular audio streaming because it can’t be paused in the same way that a song can.

In other words, this framework works by dynamically generating MP3 files that are served to the echo using SSML.  The Echo Linguistic framework generates SSML compatible MP3 files that contain a third party voice saying an inputted text.  Translation is also supported, which opens up the ability for the Echo to speak in 69 additional languages:


- German
- Albanian
- Armenian
- Bosnian
- Czech
- Danish
- Dutch
- English
- Esperanto
- Estonian
- French
- Greek
- Icelandic
- Japanese
- Javanese
- Khmer
- Korean
- Latvian
- Macedonian
- Nepali
- Norwegian
- Polish
- Portuguese
- Russian
- Serbian
- Slovak
- Spanish
- Sundanese
- Swahili
- Swedish
- Turkish
- Ukrainian
- Vietnamese
- Welsh
- English
- Afrikaans
- Albanian
- Armenian
- Bosnian
- Czech
- Danish
- Dutch
- English
- Esperanto
- Estonian
- French
- Greek
- Icelandic
- Japanese
- Javanese
- Khmer
- Korean
- Latvian
- Macedonian
- Nepali
- Norwegian
- Polish
- Portuguese
- Russian
- Serbian
- Slovak
- Spanish
- Sundanese
- Swahili
- Swedish
- Turkish
- Ukrainian
- Vietnamese
- Welsh
