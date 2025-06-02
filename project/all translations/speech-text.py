import speech_recognition as sr
from googletrans import Translator



# Initialize recognizer class (for recognizing the speech)
recognizer = sr.Recognizer()

# Initialize translator
translator = Translator()

# Function to recognize speech and translate it into user-selected language
def recognize_and_translate_user_language():
    with sr.Microphone() as source:
        print("Adjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for background noise
        print("Listening... Speak now.")
        audio = recognizer.listen(source)  # Listen for the first phrase
        
        try:
            print("Recognizing...")
            # Recognize the speech (auto-detect the language)
            text = recognizer.recognize_google(audio)
            print(f"Original text: {text}")
            
            # Detect the language of the recognized text
            detected_lang = translator.detect(text).lang
            print(f"Detected Language: {detected_lang}")
            
            # Ask the user for the destination language
            target_lang = input("Enter the destination language code (e.g., 'es' for Spanish, 'fr' for French): ")
            
            # Translate the recognized text into the user-specified language
            translated = translator.translate(text, src=detected_lang, dest=target_lang)
            print(f"Translated into {target_lang}: {translated.text}")
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
        except sr.RequestError:
            print("Could not request results from Google Speech Recognition service.")
        except Exception as e:
            print(f"An error occurred: {e}")

# Run the speech recognition and translate to the language specified by the user
recognize_and_translate_user_language()

