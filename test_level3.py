import os
from groq import Groq
from pearl_memory import ShortTermMemory

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = """
You are Pearl, an intelligent digital companion.
Keep responses natural, direct, and conversational.
Use conversational short-term context to resolve pronouns like 'he', 'she', 'it', or 'there'.
"""

def main():
    if not GROQ_API_KEY:
        print("Error: GROQ_API_KEY environment variable is missing.")
        return

    memory = ShortTermMemory(max_history=5)
    print("--- Pearl Level 3: Short-Term Memory Test ---")
    print("Type your questions below. Type 'clear' to reset memory or 'exit' to quit.\n")

    while True:
        user_input = input("You: ").strip()
        if not user_input:
            continue
            
        if user_input.lower() == "exit":
            break
        elif user_input.lower() == "clear":
            memory.clear_session()
            continue

        # 1. Add User Input to Short-Term Memory
        memory.add_message("user", user_input)

        # 2. Build Payload with Full Context
        payload = memory.get_context_payload(SYSTEM_PROMPT)

        # 3. Request LLM Completion
        try:
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=payload,
                temperature=0.7,
                max_tokens=300
            )
            response = completion.choices[0].message.content.strip()

            # 4. Add Pearl's Response back to Memory
            memory.add_message("assistant", response)

            print(f"\nPearl: {response}\n")

        except Exception as e:
            print(f"[Error]: {e}")

if __name__ == "__main__":
    main()