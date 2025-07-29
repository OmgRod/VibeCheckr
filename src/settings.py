import json

def load_settings(key=None):
    try:
        with open("settings.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            if key:
                return data.get(key, {})
            return data
    except FileNotFoundError:
        return {} if key else {}

def save_settings(key, data):
    settings = load_settings() or {}
    settings[key] = data
    with open("settings.json", "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=4)
