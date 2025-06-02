import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS  # Ensure gTTS is imported
import pyttsx3
import subprocess
import os

# Initialize the recognizer, translator, and pyttsx3 engine
recognizer = sr.Recognizer()
translator = Translator()
engine = pyttsx3.init()

# Supported languages by gTTS (without Zulu)
gtts_supported_languages = ['af', 'sq', 'am', 'ar', 'hy', 'bn', 'bs', 'ca', 'cs', 'cy', 'da', 'de', 'el', 'en', 'es', 'et', 'fi', 'fr', 'gu', 'hi', 'hr', 'hu', 'id', 'it', 'ja', 'jw', 'kn', 'ko', 'la', 'lv', 'lt', 'ml', 'mr', 'my', 'ne', 'nl', 'no', 'pl', 'pt', 'ro', 'ru', 'si', 'sk', 'sr', 'su', 'sv', 'sw', 'ta', 'te', 'th', 'tr', 'uk', 'ur', 'vi', 'zh-CN', 'zh-TW']

# Define available languages with their codes (without Zulu)
available_languages = {
    'afrikaans': 'af',
    'albanian': 'sq',
    'amharic': 'am',
    'arabic': 'ar',
    'armenian': 'hy',
    'bengali': 'bn',
    'bosnian': 'bs',
    'catalan': 'ca',
    'czech': 'cs',
    'welsh': 'cy',
    'danish': 'da',
    'german': 'de',
    'greek': 'el',
    'english': 'en',
    'spanish': 'es',
    'estonian': 'et',
    'finnish': 'fi',
    'french': 'fr',
    'gujarati': 'gu',
    'hindi': 'hi',
    'croatian': 'hr',
    'hungarian': 'hu',
    'indonesian': 'id',
    'italian': 'it',
    'japanese': 'ja',
    'javanese': 'jw',
    'kannada': 'kn',
    'korean': 'ko',
    'latin': 'la',
    'lithuanian': 'lt',
    'latvian': 'lv',
    'malayalam': 'ml',
    'marathi': 'mr',
    'nepali': 'ne',
    'dutch': 'nl',
    'norwegian': 'no',
    'polish': 'pl',
    'portuguese': 'pt',
    'romanian': 'ro',
    'russian': 'ru',
    'sinhala': 'si',
    'slovak': 'sk',
    'serbian': 'sr',
    'swahili': 'sw',
    'swedish': 'sv',
    'tamil': 'ta',
    'telugu': 'te',
    'thai': 'th',
    'turkish': 'tr',
    'ukrainian': 'uk',
    'urdu': 'ur',
    'vietnamese': 'vi',
    'xhosa': 'xh'
}

def play_audio(filename):
    if os.name == 'nt':  # If Windows
        os.startfile(filename)
    elif os.name == 'posix':
        if 'darwin' in os.uname().sysname.lower():  # macOS
            subprocess.call(['open', filename])
        else:  # Linux
            subprocess.call(['xdg-open', filename])

def translate_speech(target_language):
    if target_language == 'zu':
        print("Zulu audio is not supported.")
        return  # Skip processing for Zulu

    with sr.Microphone() as source:
        print("Listening... Please speak clearly.")
        audio = recognizer.listen(source)

        try:
            # Recognize speech using Google Speech Recognition
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")

            # Translate the recognized text to the target language
            translated = translator.translate(text, dest=target_language)
            print(f"Translated text: {translated.text}")

            # Use gTTS if the target language is supported
            if target_language in gtts_supported_languages:
                tts = gTTS(translated.text, lang=target_language)
                tts.save('output.mp3')

                # Play the audio file
                play_audio('output.mp3')
            else:
                # Use pyttsx3 for unsupported languages
                print(f"Using pyttsx3 for {target_language.upper()} as gTTS does not support it.")
                engine.say(translated.text)
                engine.runAndWait()

        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio. Please try again.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

def main():
    # Ask the user for the target language they want to translate to
    choice = input("Enter the language you want to translate to (e.g., afrikaans, spanish, etc.): ").lower()
    target_language = available_languages.get(choice)

    if target_language:
        print(f"You selected: {choice.capitalize()}.")
        translate_speech(target_language)  # Call the function to translate and output
    else:
        print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
