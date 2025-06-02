from gtts import gTTS
from googletrans import Translator
import os
import playsound

# Supported languages (case insensitive)
supported_languages = {
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
    'lithuanian': 'lt',
    'latvian': 'lv',
    'malayalam': 'ml',
    'marathi': 'mr',
    'malay': 'ms',
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
    'zulu': None  # Marking Zulu as not supported for TTS
}

# Create a translator object
translator = Translator()

# Get user input for text
text = input("Enter the text you want to convert to speech: ")
language = input("Enter the target language (e.g., Spanish, Hindi): ").strip().lower()

# Validate the language input
if language not in supported_languages:
    print(f"Language '{language}' is not supported. Please enter a valid language name.")
    print(f"Supported languages are: {', '.join(supported_languages.keys())}")
else:
    # Check if the language is supported for translation
    language_code = supported_languages[language]
    if language_code is None:
        print(f"Translation for the language '{language}' is not supported.")
    else:
        # Translate the text
        translated_text = translator.translate(text, dest=language_code).text
        print(f"Translated text: {translated_text}")

        # Create the audio file
        tts = gTTS(text=translated_text, lang=language_code, slow=False)
        tts.save("output.mp3")
        print("Audio saved as 'output.mp3'.")

        # Play the audio
        playsound.playsound("output.mp3")

        # Optionally remove the audio file
        os.remove("output.mp3")
