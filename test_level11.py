from pearl_vision import PearlVisionEngine

def main():
    vision = PearlVisionEngine()

    print("--- Pearl Level 11: Vision Pipeline Test ---\n")

    # 1. Test Screen Capture
    print("[Testing Screen Capture...]")
    success, path, msg = vision.capture_screen()
    print(f"Status: {msg}")
    if success:
        print(f"File saved to: {path}\n")

    # 2. Test Webcam Capture
    print("[Testing Webcam Capture...]")
    webcam_success, webcam_path, webcam_msg = vision.capture_webcam()
    print(f"Status: {webcam_msg}")
    if webcam_success:
        print(f"File saved to: {webcam_path}\n")

if __name__ == "__main__":
    main()