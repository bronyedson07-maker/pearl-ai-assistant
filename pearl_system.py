import os
import glob
import psutil
import webbrowser
import subprocess
import screen_brightness_control as sbc
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

class PearlSystemController:
    """
    Handles native Windows commands: process management, hardware control,
    system metrics, and local file searches.
    """

    @staticmethod
    def get_system_stats():
        """Returns CPU usage, RAM usage, and Battery status."""
        cpu = psutil.cpu_percent(interval=0.5)
        ram = psutil.virtual_memory().percent
        battery = psutil.sensors_battery()
        
        bat_str = f"{battery.percent}%" if battery else "N/A"
        charging = " (Charging)" if battery and battery.power_plugged else ""
        
        return f"CPU is at {cpu}%, RAM is at {ram}%, and battery is at {bat_str}{charging}."

    @staticmethod
    def set_volume(percent):
        """Sets master output volume (0-100%)."""
        try:
            percent = max(0, min(100, percent))
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, 0, None)
            volume = interface.QueryInterface(IAudioEndpointVolume)
            volume.SetMasterVolumeLevelScalar(percent / 100.0, None)
            return f"Volume set to {percent}%."
        except Exception as e:
            return f"Could not adjust volume: {e}"

    @staticmethod
    def set_brightness(percent):
        """Sets screen brightness level (0-100%)."""
        try:
            percent = max(0, min(100, percent))
            sbc.set_brightness(percent)
            return f"Screen brightness set to {percent}%."
        except Exception as e:
            return f"Could not adjust brightness: {e}"

    @staticmethod
    def close_app(app_name):
        """Safely closes running processes by name."""
        app_clean = app_name.lower().strip()
        closed = False
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if app_clean in proc.info['name'].lower():
                    proc.kill()
                    closed = True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        return f"Closed {app_name}." if closed else f"Could not find running app matching '{app_name}'."

    @staticmethod
    def find_file(filename, search_dir=None):
        """Searches for files in the user's Documents or Downloads folders."""
        if not search_dir:
            search_dir = os.path.expanduser("~")

        matches = []
        for root, _, files in os.walk(search_dir):
            for file in files:
                if filename.lower() in file.lower():
                    matches.append(os.path.join(root, file))
                    if len(matches) >= 3: # Limit to top 3 matches for speed
                        break
            if len(matches) >= 3:
                break

        if matches:
            return f"Found matching file: {matches[0]}"
        return f"No files matching '{filename}' were found."