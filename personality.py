import random

class PersonalityEngine:
    """
    Pearl Personality Engine (Level 4)
    Transforms raw outputs into warm, natural, human-like responses.
    Prevents repetitive corporate AI phrasing and applies response-length intelligence.
    """

    def __init__(self):
        # Acknowledgement phrase pools to vary responses naturally
        self.ACK_CONFIRM = [
            "Yep, on it.",
            "Got it.",
            "Done.",
            "Right away.",
            "Sure thing.",
            "On it."
        ]
        
        self.ACK_CHECK = [
            "Let me check that for you.",
            "One second.",
            "Give me a moment.",
            "Looking into that now."
        ]

    def format_app_launch(self, app_name: str) -> str:
        """Generates natural phrasing when launching local applications."""
        prefix = random.choice(self.ACK_CONFIRM)
        
        # Keep simple commands short and direct
        phrasings = [
            f"{prefix} Opening {app_name}.",
            f"Got it. {app_name.capitalize()} is opening.",
            f"Yep, launching {app_name} now.",
            f"Done. {app_name.capitalize()} is open."
        ]
        return random.choice(phrasings)

    def format_system_action(self, action_type: str) -> str:
        """Formats general system responses dynamically."""
        if action_type == "lock":
            return random.choice(["Locked your PC.", "PC locked.", "Got it, screen locked."])
        elif action_type == "screenshot":
            return random.choice(["Captured your screen.", "Screenshot saved.", "Done. Got the screen."])
        elif action_type == "mute":
            return random.choice(["Muted.", "System muted.", "Got it, audio muted."])
        return "Done."

    def humanize_text(self, raw_text: str, category: str = "general") -> str:
        """
        Cleans robotic language from generic text or AI model responses.
        """
        text = raw_text.strip()

        # Remove repetitive robotic openings
        robotic_triggers = [
            "Certainly! ",
            "Of course! ",
            "As an AI assistant, ",
            "I would be happy to help you with that. ",
            "Here is the answer: "
        ]
        for trigger in robotic_triggers:
            if text.startswith(trigger):
                text = text[len(trigger):]

        return text