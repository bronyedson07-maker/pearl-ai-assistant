from pearl_speech import PearlSpeechEngine

def main():
    pearl_voice = PearlSpeechEngine()
    
    pearl_voice.speak_stream("Pearl voice engine initialized. Speak into your microphone to test.")
    
    while True:
        user_input = pearl_voice.listen()
        if user_input:
            print(f"You said: {user_input}")
            
            if "stop" in user_input.lower() or "exit" in user_input.lower():
                pearl_voice.speak_stream("Catch you later.")
                break
                
            # Echo response back via sentence stream
            response = f"I heard you say: {user_input}. Everything is working smoothly."
            pearl_voice.speak_stream(response)
        else:
            print("[Silence detected... waiting for input]")

if __name__ == "__main__":
    main()