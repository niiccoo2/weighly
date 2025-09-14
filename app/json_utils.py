import json
import os

default_settings = {
    "SERIALPORT": "/dev/ttyUSB0",
    "BAUDRATE": 9600,
    "theme": "dark-blue",
    "input_mode": "manual",
    "unit": "lbs",
    "keep_name": True
}

def load_settings(SETTINGS_FILE="settings.json"):
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r") as f:
                settings = json.load(f)
                print(f"Loading {SETTINGS_FILE}:\n{settings}")
                return settings
        except (json.JSONDecodeError, OSError) as e:
            print(f"Settings file corrupted: {e}, resetting to defaults.")

    settings = default_settings.copy()
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=4)
    print(f"Made defualt file {SETTINGS_FILE}:\n{settings}")
    return settings

def save_settings(settings, SETTINGS_FILE = "settings.json"):
    print(f"Saving settings as {SETTINGS_FILE}: {settings}")
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=4)
