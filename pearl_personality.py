import re
import random

class PearlPersonalityEngine:
    """
    Transforms raw AI outputs into concise, warm, natural speech chunks.
    Strips robotic filler and enforces appropriate length.
    """
    def __init__(self):
        self.acknowledgements = [
            "On it.", "Yep, on it.", "Got it.", 
            "Give me a sec.", "Checking that now.", "Sure thing."
        ]

    def get_quick_ack(self):
        """Returns a natural, casual acknowledgement phrase."""
        return random.choice(self.acknowledgements)

    def format_response(self, text, user_query):
        """
        Refines text for natural speech and conversational flow.
        """
        # 1. Clean markdown elements
        clean = re.sub(r'[\*\#\`\_\~]', '', text)
        
        # 2. Check if the user asked a quick question or command
        query_lower = user_query.lower()
        is_simple_command = any(w in query_lower for w in ["open", "launch", "turn", "set", "mute", "volume", "brightness"])
        
        # 3. If it's a simple command, enforce ultra-concise output
        if is_simple_command and len(clean.split()) > 15:
            sentences = re.split(r'(?<=[.!?])\s+', clean)
            clean = sentences[0] # Keep only the first sentence
            
        # 4. Remove robotic AI meta-talk
        robotic_phrases = [
            "As an AI language model,", 
            "As an AI,", 
            "How may I assist you today?",
            "Certainly! ",
            "I'm happy to help. "
        ]
        for phrase in robotic_phrases:
            clean = clean.replace(phrase, "")

        return clean.strip()