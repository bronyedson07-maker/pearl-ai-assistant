import time
import speech_recognition as sr
from pearl_speech import PearlSpeechEngine

def listen_for_pearl():
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 300
    speech = PearlSpeechEngine()

    print("--- Listening continuously for 'Pearl' or 'Hey Pearl' ---")

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        while True:
            try:
                audio = recognizer.listen(source, phrase_time_limit=3)
                text = recognizer.recognize_google(audio).lower()
                
                if "pearl" in text:
                    print(f"\n⚡ Wake Word Triggered: '{text}'")
                    speech.speak_stream("Yeah? I'm here.")
            except Exception:
                pass

if __name__ == "__main__":
    listen_for_pearl()