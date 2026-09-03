import time
from pearl_wakeword import PearlWakeWordListener
from pearl_speech import PearlSpeechEngine

def on_wake():
    """Callback function executed immediately upon wake word detection."""
    speech = PearlSpeechEngine()
    print("Pearl: Yeah? I'm listening.")
    speech.speak_stream("Yeah? I'm listening.")

def main():
    print("--- Pearl Level 5: Wake Word Test ---")
    print("Say 'Jarvis' or your wake word to trigger Pearl. Press Ctrl+C to exit.\n")
    
    listener = PearlWakeWordListener(keyword="jarvis")
    listener.start_listening(on_wake_callback=on_wake)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nExiting Level 5 Test...")
        listener.stop_listening()

if __name__ == "__main__":
    main()