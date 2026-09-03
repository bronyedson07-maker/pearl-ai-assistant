import re
import threading
import pyttsx3
import speech_recognition as sr

class PearlSpeechEngine:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.recognizer.pause_threshold = 0.8
        self.recognizer.energy_threshold = 300
        
        self.engine = pyttsx3.init()
        self.configure_voice()
        self.is_speaking = False

    def configure_voice(self):
        """Sets up a natural voice profile."""
        try:
            self.engine.setProperty('rate', 170)
            self.engine.setProperty('volume', 1.0)
            
            voices = self.engine.getProperty('voices')
            for v in voices:
                if "zira" in v.name.lower() or "female" in v.name.lower():
                    self.engine.setProperty('voice', v.id)
                    break
        except Exception as e:
            print(f"[Speech Config Warning]: {e}")

    def listen(self):
        """Captures microphone input."""
        with sr.Microphone() as source:
            print("\n[Pearl is listening...]")
            self.recognizer.adjust_for_ambient_noise(source, duration=0.4)
            try:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                text = self.recognizer.recognize_google(audio)
                return text.strip()
            except Exception:
                return None

    def speak_stream(self, text):
        """Streams text chunks to speech asynchronously."""
        def _stream():
            self.is_speaking = True
            chunks = re.split(r'(?<=[.!?])\s+', text)
            for chunk in chunks:
                if not chunk.strip():
                    continue
                clean_chunk = re.sub(r'[\*\#\`\_\~]', '', chunk)
                self.engine.say(clean_chunk)
                self.engine.runAndWait()
            self.is_speaking = False

        threading.Thread(target=_stream, daemon=True).start()

    def stop_speaking(self):
        """Interrupts speech immediately."""
        if self.is_speaking:
            self.engine.stop()
            self.is_speaking = False