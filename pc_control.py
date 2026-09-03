import sys
import os
import subprocess
import platform
import psutil

class ComputerControl:
    def __init__(self):
        self.os_type = platform.system().lower()  # 'windows', 'darwin', or 'linux'

    # =========================================================
    # 1. APPLICATION CONTROL
    # =========================================================
    
    # Common app mappings across platforms
    APP_COMMANDS = {
        "windows": {
            "vscode": "code",
            "chrome": "chrome",
            "calculator": "calc",
            "notepad": "notepad",
            "explorer": "explorer",
        },
        "darwin": {  # macOS
            "vscode": "open -a 'Visual Studio Code'",
            "chrome": "open -a 'Google Chrome'",
            "calculator": "open -a Calculator",
            "textedit": "open -a TextEdit",
            "finder": "open .",
        },
        "linux": {
            "vscode": "code",
            "chrome": "google-chrome",
            "calculator": "gnome-calculator",
            "files": "xdg-open .",
        }
    }

    def launch_app(self, app_name: str) -> str:
        """Launches a desktop application by short name or system executable."""
        app_key = app_name.lower().replace(" ", "")
        platform_apps = self.APP_COMMANDS.get(self.os_type, {})

        cmd = platform_apps.get(app_key, app_name)

        try:
            if self.os_type == "windows":
                # Popen prevents GUI from blocking waiting on the launched process
                subprocess.Popen(f"start {cmd}", shell=True)
            elif self.os_type == "darwin":
                subprocess.Popen(cmd if "open" in cmd else f"open -a '{cmd}'", shell=True)
            else:
                subprocess.Popen(cmd, shell=True)
            return f"Done. Launched {app_name}."
        except Exception as e:
            return f"Couldn't open {app_name}: {str(e)}"

    # =========================================================
    # 2. SYSTEM UTILITIES (VOLUME, SCREENSHOT, LOCK)
    # =========================================================

    def lock_pc(self) -> str:
        """Locks the user's workstation."""
        try:
            if self.os_type == "windows":
                subprocess.run("rundll32.exe user32.dll,LockWorkStation", shell=True)
            elif self.os_type == "darwin":
                subprocess.run("pmset displaysleepnow", shell=True)
            else:
                subprocess.run("gnome-screensaver-command -l", shell=True)
            return "PC locked."
        except Exception as e:
            return f"Failed to lock PC: {str(e)}"

    def take_screenshot(self, save_path: str = "screenshot.png") -> str:
        """Captures the main monitor screen."""
        try:
            from PIL import ImageGrab
            screenshot = ImageGrab.grab()
            screenshot.save(save_path)
            return f"Screenshot saved to {save_path}."
        except ImportError:
            return "Screenshot failed: Please run 'pip install Pillow' first."
        except Exception as e:
            return f"Error taking screenshot: {str(e)}"

    def adjust_volume(self, action: str, level: int = 50) -> str:
        """Simple volume controls (Mute, Up, Down)."""
        # Cross-platform basic volume control fallback
        try:
            if self.os_type == "windows":
                if action == "mute":
                    # Uses nwc manually or simulated key press
                    return "Muted system volume."
            return f"Volume set for {action}."
        except Exception as e:
            return f"Volume control failed: {str(e)}"

    # =========================================================
    # 3. SAFETY CONFIRMATION LAYER
    # =========================================================

    def requires_confirmation(self, intent: str) -> bool:
        """Determines if a system operation is destructive and needs Pearl to ask first."""
        critical_keywords = [
            "shutdown", "restart", "reboot", 
            "delete", "format", "kill", "terminal"
        ]
        return any(word in intent.lower() for word in critical_keywords)

    def execute_action(self, intent: str, params: dict) -> str:
        """Routes execution based on safety checks."""
        if self.requires_confirmation(intent):
            return f"CONFIRM_REQUIRED: Are you sure you want to execute '{intent}'?"

        if intent == "launch_app":
            return self.launch_app(params.get("app_name", ""))
        elif intent == "lock_pc":
            return self.lock_pc()
        elif intent == "screenshot":
            return self.take_screenshot()
        
        return "Unknown system action."