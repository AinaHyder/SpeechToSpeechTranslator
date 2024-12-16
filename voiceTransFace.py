import cv2
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import playsound
import os
import threading

# Initialize the recognizer and translator
recognizer = sr.Recognizer()
translator = Translator()

# Initialize video capture
video_cap = cv2.VideoCapture(0)

def translate_and_speak():
    global translated_text
    while True:
        # Capture frame-by-frame
        ret, video_data = video_cap.read()

        # Check if the frame was captured correctly
        if not ret:
            print("Error: Could not read frame.")
            break

        # Display prompt on the camera screen
        cv2.putText(video_data, "Speak now (input in your chosen language)...", (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

        # Show the current frame
        cv2.imshow("video_live", video_data)

        # Use the microphone as input
        with sr.Microphone() as source:
            # Adjust for ambient noise and pause for a moment
            recognizer.adjust_for_ambient_noise(source)
            print("Listening...")
            audio = recognizer.listen(source)

            try:
                # Recognize speech using Google Web Speech API
                text = recognizer.recognize_google(audio, language="en")  # Change to your preferred language
                print(f"Original: {text}")

                # Translate to English
                translation = translator.translate(text, dest="zh-CN")  # Change to the target language
                translated_text = translation.text
                print(f"Translation: {translated_text}")

                # Convert text to speech
                converted_audio = gTTS(text=translated_text, lang='zh-CN', slow=False)
                converted_audio.save("translation.mp3")

                # Play the converted audio
                playsound.playsound("translation.mp3")
                os.remove("translation.mp3")  # Optionally remove the audio file

            except sr.UnknownValueError:
                translated_text = "Could not understand the audio"
            except sr.RequestError as e:
                translated_text = f"Could not request results; {e}"

        # Display translation on the camera screen
        cv2.putText(video_data, f"Translation: {translated_text}", (10, 70), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

        # Show the updated frame
        cv2.imshow("video_live", video_data)

        # Exit the loop when the 'a' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('a'):
            break

# Run the translate_and_speak function in a separate thread
thread = threading.Thread(target=translate_and_speak)
thread.start()

# Keep the main thread alive
while thread.is_alive():
    pass

# Release the video capture object and close all windows
video_cap.release()
cv2.destroyAllWindows()
