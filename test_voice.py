import pyttsx3
import speech_recognition as sr
import whisper
import os

# 1. Initialize Text-to-Speech Engine with Maximum Volume
engine = pyttsx3.init()
engine.setProperty('volume', 1.0)  # Max volume (0.0 to 1.0)
engine.setProperty('rate', 160)     # Slightly slower, clearer speed

def speak(text):
    print(f"\nAssistant: {text}")
    engine.say(text)
    engine.runAndWait()

# 2. Load local Whisper model
print("Loading speech recognition model...")
model = whisper.load_model("base")

# 3. Capture Voice Input
recognizer = sr.Recognizer()

speak("Ready! Take your time and speak into the microphone.")

with sr.Microphone() as source:
    print("\n[LISTENING...] Adjusting for background noise...")
    recognizer.adjust_for_ambient_noise(source, duration=1)
    
    print("[SPEAK NOW...] Listening indefinitely until you pause...")
    # Removed initial timeout; phrase_time_limit allows up to 15s of continuous speech
    audio = recognizer.listen(source, timeout=None, phrase_time_limit=15)
    
    print("[PROCESSING...] Transcribing your voice locally...")

    # Save audio temporarily
    with open("temp_input.wav", "wb") as f:
        f.write(audio.get_wav_data())

try:
    # 4. Transcribe audio using Whisper
    result = model.transcribe("temp_input.wav")
    user_text = result["text"].strip()
    
    print(f"\nYou said: '{user_text}'")
    speak(f"I heard you say: {user_text}")

except Exception as e:
    print(f"Error: {e}")
    speak("Sorry, I had trouble processing that audio.")

finally:
    # Clean up temp file
    if os.path.exists("temp_input.wav"):
        os.remove("temp_input.wav")