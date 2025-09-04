import json
import os

default_settings = {
    "SERIALPORT": "/dev/ttyUSB0",
    "BAUDRATE": 9600,
    "theme": "dark-blue",
    "input_mode": "manual",
    "unit": "lbs",
    "auto_remove_name": True
}

def load_settings(SETTINGS_FILE="settings.json"):
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            print("Settings file corrupted, resetting to defaults.")

    settings = default_settings.copy()
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=4)
    return settings

def save_settings(settings, SETTINGS_FILE = "settings.json"):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=4)
