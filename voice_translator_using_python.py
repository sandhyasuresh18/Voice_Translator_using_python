from gtts import gTTS
import os
from googletrans import Translator
import speech_recognition as sr
import tkinter as tk
from tkinter import messagebox

recognizer = sr.Recognizer()

# Function to recognize and translate speech
def trans(langinput):
    translator = Translator()

    with sr.Microphone() as source:
        print('Cleaning the background noises...')
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print('Waiting for your message...')
        audio = recognizer.listen(source, timeout=5)
        print('Done recording')

    try:
        print('Recognizing...')
        result = recognizer.recognize_google(audio, language='en')
        print(f"Recognized text: {result}")

        # Translate the recognized text
        translated_text = translator.translate(result, dest=langinput).text
        print(f"Translated text: {translated_text}")

        # Display translated text in the UI
        translation_label.config(text=f"Translated: {translated_text}")

        # Use gTTS to speak the translated text
        tts = gTTS(text=translated_text, lang=langinput)
        tts.save("output.mp3")
        os.system("start output.mp3")  # Play the generated audio file

    except Exception as ex:
        print(f"Error: {ex}")
        messagebox.showerror("Error", f"An error occurred: {ex}")

# Function to be called when the user presses the button
def on_translate_button_click():
    langinput = lang_entry.get()  # Get the language code from the entry field
    if langinput:
        trans(langinput)
    else:
        messagebox.showwarning("Input Error", "Please enter a valid language code.")

# Set up the Tkinter UI
root = tk.Tk()
root.title("Voice Translator")

# Set up UI elements
label = tk.Label(root, text="Voice Translator", font=("Arial", 20))
label.pack(pady=10)

instruction_label = tk.Label(root, text="Enter the language code (e.g., 'fr' for French, 'ta' for Tamil):")
instruction_label.pack(pady=5)

lang_entry = tk.Entry(root, font=("Arial", 14))
lang_entry.pack(pady=5)

translate_button = tk.Button(root, text="Translate and Speak", font=("Arial", 14), command=on_translate_button_click)
translate_button.pack(pady=10)

translation_label = tk.Label(root, text="Translated: ", font=("Arial", 12), wraplength=300)
translation_label.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()
