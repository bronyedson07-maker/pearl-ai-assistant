import os
from datetime import datetime
from openai import OpenAI
from pc_control import ComputerControl
from router import RequestRouter
from personality import PersonalityEngine
from database import MemoryDatabase

class AssistantBrain:
    def __init__(self):
        self.pc = ComputerControl()
        self.router = RequestRouter()
        self.personality = PersonalityEngine()
        self.db = MemoryDatabase()
        
        # Reads OPENAI_API_KEY from environment variables safely
        api_key = os.environ.get("OPENAI_API_KEY")
        
        if not api_key:
            print("⚠️ Warning: OPENAI_API_KEY environment variable not found!")
            
        self.client = OpenAI(api_key=api_key)
        
        self.system_prompt = (
            "You are Pearl, a helpful, polite, and intelligent AI voice assistant for Edson. "
            "Keep your answers concise, clear, and direct suitable for text-to-speech."
        )

    def process_query(self, user_query: str) -> str:
        raw_query = user_query.strip()
        if not raw_query:
            return "I didn't catch that."

        query = raw_query.lower()

        # 1. Local PC Controls
        intent = self.router.classify_intent(query)
        if intent == RequestRouter.INTENT_PC_CONTROL:
            if query.startswith(("open ", "launch ", "start ")):
                app_name = query.replace("open ", "").replace("launch ", "").replace("start ", "").replace("pearl ", "").strip()
                status = self.pc.launch_app(app_name)
                res = self.personality.format_app_launch(app_name) if "Done" in status else status
                self.db.save_message("user", raw_query)
                self.db.save_message("assistant", res)
                return res
            elif "lock" in query:
                self.pc.lock_pc()
                res = self.personality.format_system_action("lock")
                self.db.save_message("user", raw_query)
                self.db.save_message("assistant", res)
                return res

        # 2. Save User Query
        self.db.save_message("user", raw_query)

        # 3. Retrieve DB Memory Context
        past_history = self.db.get_recent_history(limit=10)
        messages = [{"role": "system", "content": self.system_prompt}] + past_history

        # 4. Generate AI Output
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                temperature=0.7,
                max_tokens=150
            )
            ai_message = response.choices[0].message.content.strip()
        except Exception as e:
            ai_message = f"I ran into an issue connecting to my brain: {str(e)}"

        # 5. Save Response
        self.db.save_message("assistant", ai_message)
        return ai_message