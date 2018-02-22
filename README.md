# Echo Linguistics
#### Using Alexa's Speech Synthesis Markup Language Support to Extend Amazon Echo Voice Capabilities

### How does this work?

The Alexa Skill Kit offers 2 ways for developers to play audio on Amazon Echo devices.

- Audio Streaming (Spotify, Amazon Music, etc.)

- Speech Synthesis Markup Support (Buzzer in games, timer going off, etc.)




Amazon describes SSML as the following:
> SSML is a markup language that provides a standard way to mark up text for the generation of synthetic speech


With SSML, developers can tell Alexa to enunciate words a certain way (Tomato vs. Tomoto).  SSML can also be used to play audio files on the echo, but it differs from regular audio streaming because it can’t be paused in the same way that a song can.

In other words, this framework works by dynamically generating MP3 files that are served to the echo using SSML.  The Echo Linguistic framework generates SSML compatible MP3 files that contain a third party voice saying an inputted text.  Translation is also supported, which opens up the ability for the Echo to speak in 69 additional languages.

### Requirements

- A PUBLIC Amazon S3 Bucket

- AWS Access keys with the following permissions:

`
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "s3:*",
            "Resource": "*"
        }
    ]
}
`


### How do I use Echo Linguistics?

After cloning the repository and fulfilling all requirements run the following commands:

` $ pip install -r requirements.txt `

` $ python config.py `

The program will then ask you for configuration details.  After the prompt has finished and verified the credentials with a test upload, the lambda function is ready to be deployed.

The easiest way to deploy the Lambda function is to compress all of the files located in sampleSkill/lambda/ into a ZIP file, and "Upload as ZIP" in AWS Lambda.

After the Lambda function has been successfully deployed, the sample skill function will need to be uploaded to the alexa skill creator.

You can either use ASK CLI or manually create a skill and post the contents of sampleSkill/models/en-US.json into the "Code Editor" section of the Alexa Skills Kit web app.


After saving/building the skill, you should now have a functioning Alexa skill that can utilize third party voices on the amazon echo.

To test the skill, say:

"Open Echo Linguistics"

"Tell me something in {language}"

### Supported Languages

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
