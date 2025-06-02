import tkinter as tk
from tkinter import ttk, messagebox
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import playsound
import os

# Initialize the recognizer and translator
recognizer = sr.Recognizer()
translator = Translator()

# Supported languages for gTTS
supported_languages = {
    'afrikaans': 'af', 'albanian': 'sq', 'amharic': 'am', 'arabic': 'ar', 'armenian': 'hy',
    'bengali': 'bn', 'bosnian': 'bs', 'catalan': 'ca', 'czech': 'cs', 'welsh': 'cy',
    'danish': 'da', 'german': 'de', 'greek': 'el', 'english': 'en', 'spanish': 'es',
    'estonian': 'et', 'finnish': 'fi', 'french': 'fr', 'gujarati': 'gu', 'hindi': 'hi',
    'croatian': 'hr', 'hungarian': 'hu', 'indonesian': 'id', 'italian': 'it', 'japanese': 'ja',
    'javanese': 'jw', 'kannada': 'kn', 'korean': 'ko', 'lithuanian': 'lt', 'latvian': 'lv',
    'malayalam': 'ml', 'marathi': 'mr', 'malay': 'ms', 'dutch': 'nl', 'norwegian': 'no',
    'polish': 'pl', 'portuguese': 'pt', 'romanian': 'ro', 'russian': 'ru', 'sinhala': 'si',
    'slovak': 'sk', 'serbian': 'sr', 'swahili': 'sw', 'swedish': 'sv', 'tamil': 'ta',
    'telugu': 'te', 'thai': 'th', 'turkish': 'tr', 'ukrainian': 'uk', 'urdu': 'ur',
    'vietnamese': 'vi', 'zulu': None  # Marking Zulu as not supported for TTS
}

# Function for Speech-to-Text with Translation
def speech_to_text():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio)
            input_box.delete(1.0, tk.END)  # Clear text box
            input_box.insert(tk.END, text)  # Display the recognized text
            
            # Translate the recognized text to the selected target language
            target_lang_code = supported_languages[target_lang.get().lower()]
            translated_text = translator.translate(text, dest=target_lang_code).text
            translated_box.delete(1.0, tk.END)  # Clear translated text box
            translated_box.insert(tk.END, translated_text)  # Show translated text in the output box
        except sr.UnknownValueError:
            input_box.insert(tk.END, "Sorry, I did not understand that.")
        except sr.RequestError:
            input_box.insert(tk.END, "Request failed, check your internet.")

# Function for Text-to-Speech with Translation
def text_to_speech():
    text = input_box.get(1.0, tk.END).strip()
    target_language = target_lang.get().lower()  # Get the target language from the dropdown

    if not text:
        messagebox.showwarning("Input Error", "Please enter some text for speech synthesis.")
        return

    if target_language not in supported_languages:
        messagebox.showerror("Language Error", f"Language '{target_language}' is not supported for TTS.")
        return
    
    language_code = supported_languages[target_language]
    
    if language_code is None:
        messagebox.showerror("Language Error", f"TTS for the language '{target_language}' is not supported.")
    else:
        # Translate the text
        translated_text = translator.translate(text, dest=language_code).text
        translated_box.delete(1.0, tk.END)
        translated_box.insert(tk.END, translated_text)
        
        try:
            # Create the audio file
            tts = gTTS(text=translated_text, lang=language_code, slow=False)
            tts.save("output.mp3")
            
            # Play the audio file
            playsound.playsound("output.mp3")
            
            # Optionally delete the audio file after playing
            os.remove("output.mp3")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during TTS: {str(e)}")

# Function for Text-to-Text translation
def text_to_text():
    text = input_box.get(1.0, tk.END).strip()
    target_lang_code = supported_languages[target_lang.get().lower()]
    if text:
        translated_text = translator.translate(text, dest=target_lang_code).text
        translated_box.delete(1.0, tk.END)
        translated_box.insert(tk.END, translated_text)
    else:
        print("No text provided for translation.")

# Function for Speech-to-Speech translation
def speech_to_speech():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio)
            input_box.delete(1.0, tk.END)  # Clear text box
            input_box.insert(tk.END, text)  # Display the recognized text
            target_lang_code = supported_languages[target_lang.get().lower()]
            translated_text = translator.translate(text, dest=target_lang_code).text

            # Generate speech for translated text
            if target_lang_code in supported_languages.values():
                tts = gTTS(translated_text, lang=target_lang_code)
                tts.save("translated_output.mp3")
                playsound.playsound("translated_output.mp3")
                os.remove("translated_output.mp3")
        except sr.UnknownValueError:
            input_box.insert(tk.END, "Sorry, I did not understand that.")
        except sr.RequestError:
            input_box.insert(tk.END, "Request failed, check your internet.")

# Clear text box function
def clear_text():
    input_box.delete(1.0, tk.END)            # Clear the input text box
    translated_box.delete(1.0, tk.END)       # Clear the translated text box
    operation_mode.set("")                    # Deselect all radio buttons
    target_lang.set("")                       # Reset the target language to None

# Main Application GUI
root = tk.Tk()
root.title("VoiceFlow")

# Add title
title_label = tk.Label(root, text="A Multilingual Speech and Text Conversion Tool", 
                       font=('Arial', 24, 'bold'), fg="#4A90E2", bg="#F5F5F5")
title_label.pack(pady=20)
title_label.config(anchor=tk.CENTER)

# Center the main frame
main_frame = ttk.Frame(root, padding="20")
main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# Radio buttons for selecting the operation mode
operation_mode = tk.StringVar(value="")  # Set to empty string for no default selection
ttk.Label(main_frame, text="Choose Operation:", font=('Arial', 12, 'bold')).grid(row=0, column=0, sticky=tk.W, pady=5)
ttk.Radiobutton(main_frame, text="Speech-to-Text", variable=operation_mode, value="Speech-to-Text").grid(row=1, column=0, sticky=tk.W)
ttk.Radiobutton(main_frame, text="Text-to-Speech", variable=operation_mode, value="Text-to-Speech").grid(row=1, column=1, sticky=tk.W)
ttk.Radiobutton(main_frame, text="Text-to-Text", variable=operation_mode, value="Text-to-Text").grid(row=2, column=0, sticky=tk.W)
ttk.Radiobutton(main_frame, text="Speech-to-Speech", variable=operation_mode, value="Speech-to-Speech").grid(row=2, column=1, sticky=tk.W)

# Optional: Add a message below the radio buttons
#ttk.Label(main_frame, text="Please select an operation mode.", font=('Arial', 10)).grid(row=3, column=0, columnspan=2, pady=5)

# Target Language Label and Dropdown
ttk.Label(main_frame, text="Select Target Language:", font=('Arial', 12, 'bold')).grid(row=4, column=0, sticky=tk.W, pady=10)
target_lang = tk.StringVar(value="French")
lang_dropdown = ttk.Combobox(main_frame, textvariable=target_lang, values=list(supported_languages.keys()), state="readonly", font=('Arial', 12))
lang_dropdown.grid(row=5, column=0, columnspan=2, pady=5)

# Input and Translated Text Boxes
ttk.Label(main_frame, text="Enter Text:", font=('Arial', 12, 'bold')).grid(row=6, column=0, sticky=tk.W, pady=5)
input_box = tk.Text(main_frame, height=6, width=50, font=('Arial', 12))
input_box.grid(row=7, column=0, columnspan=2)

ttk.Label(main_frame, text="Translated Output:", font=('Arial', 12, 'bold')).grid(row=8, column=0, sticky=tk.W, pady=5)
translated_box = tk.Text(main_frame, height=6, width=50, font=('Arial', 12))
translated_box.grid(row=9, column=0, columnspan=2)

# Execute button
execute_button = ttk.Button(main_frame, text="Execute", command=lambda: {
    "Speech-to-Text": speech_to_text,
    "Text-to-Speech": text_to_speech,
    "Text-to-Text": text_to_text,
    "Speech-to-Speech": speech_to_speech
}.get(operation_mode.get(), lambda: messagebox.showwarning("Selection Error", "Please select an operation mode."))())
execute_button.grid(row=10, column=0, pady=20)

# Clear button
clear_button = ttk.Button(main_frame, text="Clear", command=clear_text)
clear_button.grid(row=10, column=1, pady=20)

# Start the application
root.mainloop()