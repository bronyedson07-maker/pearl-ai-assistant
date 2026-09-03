import time

class ShortTermMemory:
    """
    Manages active session context, dynamic topic tracking,
    and recent message history for natural multi-turn conversations.
    """
    def __init__(self, max_history=10):
        self.max_history = max_history
        self.history = []
        self.active_context = {
            "last_subject": None,
            "last_action": None,
            "user_emotion": "neutral"
        }

    def add_message(self, role, content):
        self.history.append({
            "role": role,
            "content": content,
            "timestamp": time.time()
        })
        
        if len(self.history) > self.max_history * 2:
            self.history = self.history[-self.max_history * 2:]

    def get_context_payload(self, system_prompt):
        messages = [{"role": "system", "content": system_prompt}]
        for msg in self.history:
            messages.append({"role": msg["role"], "content": msg["content"]})
        return messages

    def update_subject(self, subject):
        self.active_context["last_subject"] = subject

    def clear_session(self):
        self.history.clear()
        self.active_context = {"last_subject": None, "last_action": None, "user_emotion": "neutral"}
        print("[Pearl Memory: Short-term context cleared]")