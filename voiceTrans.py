import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import playsound
import os

# Initialize recognizer and translator
recognizer = sr.Recognizer()
translator = Translator()

# Use the microphone as input
with sr.Microphone() as source:
    print("Speak now (input in English)...")
    audio = recognizer.listen(source)

    try:
        # Recognize speech using Google Web Speech API
        # speak in......
        text = recognizer.recognize_google(audio, language="ur")
        print(f"Original (English): {text}")

        # translate to.......
        # Translate to French

        translation = translator.translate(text, dest="en")
        print(f"Translation : {translation.text}")

        # Convert text to speech
        converted_audio = gTTS(text=translation.text, lang='en', slow=False)
        converted_audio.save("translation.mp3")

        # Play the converted audio
        playsound.playsound("translation.mp3")
        
        # Optionally, remove the audio file after playing
        os.remove("translation.mp3")

    except sr.UnknownValueError:
        print("Could not understand the audio")
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
