import json
import os

default_settings = {
    "SERIALPORT": "/dev/ttyUSB0",
    "BAUDRATE": 9600,
    "theme": "dark-blue",
    "input_mode": "scale"
}

def load_settings(SETTINGS_FILE = "settings.json"):
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    return default_settings.copy()

def save_settings(settings, SETTINGS_FILE = "settings.json"):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=4)
