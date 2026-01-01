import os
import json

def load_settings():
    """config/settings.json 불러오기"""
    path = os.path.join(os.path.dirname(__file__), "..", "config", "settings.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)