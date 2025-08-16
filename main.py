import os
import tkinter as tk
from tkinter import ttk, messagebox
import threading

from deep_translator import GoogleTranslator
import speech_recognition as sr
from elevenlabs import play
from elevenlabs.client import ElevenLabs

# Initialize ElevenLabs client with API key from environment
ELEVEN_API_KEY = os.getenv("ELEVENLABS_API_KEY")
if ELEVEN_API_KEY:
    eleven_client = ElevenLabs(api_key=ELEVEN_API_KEY)
else:
    eleven_client = None

# Default voice and model ids from ElevenLabs
VOICE_ID = "JBFqnCBsd6RMkjVDRZzb"  # Example voice
MODEL_ID = "eleven_multilingual_v2"

recognizer = sr.Recognizer()

# Translation functions

def translate_text(text, source_lang, target_lang):
    try:
        return GoogleTranslator(source=source_lang, target=target_lang).translate(text)
    except Exception as e:
        messagebox.showerror("Translation Error", str(e))
        return ""

# Speech recognition

def transcribe_speech(language):
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio, language=language)
    except Exception as e:
        messagebox.showerror("Speech Recognition Error", str(e))
        return ""

# Text to speech

def speak_text(text, voice_id=VOICE_ID, model_id=MODEL_ID):
    if not eleven_client:
        messagebox.showwarning("ElevenLabs", "API key not set. Set ELEVENLABS_API_KEY env variable.")
        return
    try:
        audio = eleven_client.text_to_speech.convert(
            text=text,
            voice_id=voice_id,
            model_id=model_id,
            output_format="mp3_44100_128",
        )
        play(audio)
    except Exception as e:
        messagebox.showerror("TTS Error", str(e))

# GUI functions

def record_bosnian():
    bosnian_text.delete(1.0, tk.END)
    bosnian_text.insert(tk.END, "Listening...")
    def task():
        text = transcribe_speech("bs")
        bosnian_text.delete(1.0, tk.END)
        bosnian_text.insert(tk.END, text)
        english_text.delete(1.0, tk.END)
        english_text.insert(tk.END, translate_text(text, "bs", "en"))
    threading.Thread(target=task).start()


def record_english():
    english_text.delete(1.0, tk.END)
    english_text.insert(tk.END, "Listening...")
    def task():
        text = transcribe_speech("en-US")
        english_text.delete(1.0, tk.END)
        english_text.insert(tk.END, text)
        bosnian_text.delete(1.0, tk.END)
        bosnian_text.insert(tk.END, translate_text(text, "en", "bs"))
    threading.Thread(target=task).start()


def speak_bosnian():
    text = bosnian_text.get(1.0, tk.END).strip()
    if text:
        threading.Thread(target=speak_text, args=(text,)).start()


def speak_english():
    text = english_text.get(1.0, tk.END).strip()
    if text:
        threading.Thread(target=speak_text, args=(text,)).start()

# UI setup
root = tk.Tk()
root.title("Bosnian-English Translator")
root.configure(bg="#1e1e1e")

style = ttk.Style()
style.theme_use("clam")
style.configure("TLabel", foreground="white", background="#1e1e1e")
style.configure("TButton", foreground="white", background="#333333")

# Bosnian widgets
bosnian_label = ttk.Label(root, text="Bosnian")
bosnian_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

bosnian_text = tk.Text(root, height=6, width=40, bg="#2d2d2d", fg="white")
bosnian_text.grid(row=1, column=0, padx=10, pady=5)

bosnian_buttons = ttk.Frame(root)
bosnian_buttons.grid(row=2, column=0, pady=5)

tt1 = ttk.Button(bosnian_buttons, text="Record Bosnian", command=record_bosnian)
tt1.grid(row=0, column=0, padx=5)

tt2 = ttk.Button(bosnian_buttons, text="Speak", command=speak_bosnian)
tt2.grid(row=0, column=1, padx=5)

# English widgets
english_label = ttk.Label(root, text="English")
english_label.grid(row=0, column=1, padx=10, pady=5, sticky="w")

english_text = tk.Text(root, height=6, width=40, bg="#2d2d2d", fg="white")
english_text.grid(row=1, column=1, padx=10, pady=5)

english_buttons = ttk.Frame(root)
english_buttons.grid(row=2, column=1, pady=5)

tt3 = ttk.Button(english_buttons, text="Record English", command=record_english)
tt3.grid(row=0, column=0, padx=5)

tt4 = ttk.Button(english_buttons, text="Speak", command=speak_english)
tt4.grid(row=0, column=1, padx=5)

root.mainloop()
