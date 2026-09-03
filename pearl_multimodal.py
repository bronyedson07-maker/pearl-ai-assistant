import base64
import os
import re
from groq import Groq

class PearlVisionAnalyzer:
    """
    Sends captured images (screen or webcam) to Groq's active multimodal 
    vision endpoint for real-time visual analysis.
    """
    def __init__(self, api_key):
        self.client = Groq(api_key=api_key)

    def _encode_image(self, image_path):
        """Encodes an image file into a base64 string."""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def analyze_image(self, image_path, user_prompt="What is in this image?"):
        """Sends the base64 encoded image and user prompt to the vision model."""
        if not os.path.exists(image_path):
            return f"Error: Image file not found at '{image_path}'."

        try:
            base64_image = self._encode_image(image_path)
            
            response = self.client.chat.completions.create(
                model="qwen/qwen3.6-27b",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text", 
                                "text": f"Directly describe what you see without showing any internal chain-of-thought or reasoning: {user_prompt}"
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                temperature=0.3,
                max_tokens=1000
            )
            raw_text = response.choices[0].message.content.strip()

            # Clean out any leftover reasoning tags if present
            clean_text = re.sub(r'<think>.*?</think>', '', raw_text, flags=re.DOTALL).strip()
            
            if "<think>" in clean_text:
                clean_text = clean_text.split("<think>")[0].strip()
            if "</think>" in clean_text:
                clean_text = clean_text.split("</think>")[-1].strip()

            return clean_text if clean_text else raw_text

        except Exception as e:
            return f"Vision processing error: {e}"