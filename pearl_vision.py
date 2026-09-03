import os
import cv2
import mss
from PIL import Image

class PearlVisionEngine:
    """
    Handles screen captures and webcam snapshot processing for Pearl using
    mss for reliable hardware-accelerated screen capture.
    """
    
    @staticmethod
    def _get_save_dir():
        """Ensures the save directory exists before saving files."""
        pictures_dir = os.path.join(os.path.expanduser("~"), "Pictures")
        os.makedirs(pictures_dir, exist_ok=True)
        return pictures_dir

    @classmethod
    def capture_screen(cls):
        """Captures the active primary display using mss to prevent black screen issues."""
        try:
            save_dir = cls._get_save_dir()
            filepath = os.path.join(save_dir, "pearl_screen_temp.png")
            
            with mss.mss() as sct:
                # Get the primary monitor dimensions
                monitor = sct.monitors[1] if len(sct.monitors) > 1 else sct.monitors[0]
                sct_img = sct.grab(monitor)
                
                # Convert raw mss image to PIL Image and save
                img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
                img.save(filepath, "PNG")
                
            return True, filepath, "Captured screen successfully."
        except Exception as e:
            return False, None, f"Failed to capture screen: {e}"

    @classmethod
    def capture_webcam(cls):
        """Captures a single frame snapshot from the primary webcam."""
        try:
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                return False, None, "Could not open webcam."

            for _ in range(5):
                ret, frame = cap.read()

            cap.release()

            if ret:
                save_dir = cls._get_save_dir()
                filepath = os.path.join(save_dir, "pearl_webcam_temp.png")
                cv2.imwrite(filepath, frame)
                return True, filepath, "Captured webcam snapshot successfully."
            
            return False, None, "Failed to capture video frame."
        except Exception as e:
            return False, None, f"Webcam error: {e}"