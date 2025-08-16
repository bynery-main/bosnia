# Bosnian-English Translator

This project provides a simple desktop application that translates between Bosnian and English. It supports speech recognition and uses the [ElevenLabs](https://elevenlabs.io) API for text-to-speech output.

## Features

- Transcribe spoken Bosnian or English using the microphone.
- Translate text between Bosnian (`bs`) and English (`en`).
- Convert translated text to speech via ElevenLabs voices.
- Dark themed Tkinter UI.

## Setup

1. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

2. **Set ElevenLabs API key**

   ```bash
   export ELEVENLABS_API_KEY="your_key_here"
   ```

3. **Run the app**

   ```bash
   python main.py
   ```

## Notes

- Microphone access is required for speech recognition.
- The `ELEVENLABS_API_KEY` needs Text-to-Speech access enabled on your ElevenLabs account.
