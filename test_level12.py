import os
from pearl_multimodal import PearlVisionAnalyzer

# Fetch the key safely from environment variables
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def main():
    if not GROQ_API_KEY:
        print("Error: GROQ_API_KEY environment variable is missing.")
        return

    analyzer = PearlVisionAnalyzer(api_key=GROQ_API_KEY)
    
    # Path to the screen capture saved in Level 11
    screen_path = os.path.join(os.path.expanduser("~"), "Pictures", "pearl_screen_temp.png")

    print("--- Pearl Level 12: Multimodal Vision Test ---")
    print(f"Analyzing image: {screen_path}\n")

    prompt = "Describe briefly what is displayed on this screen."
    analysis = analyzer.analyze_image(screen_path, user_prompt=prompt)

    print("Pearl's Visual Analysis:")
    print("-" * 45)
    print(analysis)
    print("-" * 45)

if __name__ == "__main__":
    main()