import os
import json

THEMES_DIR = os.path.join(os.path.dirname(__file__), "themes")

def load_themes():
    themes = {}
    for filename in os.listdir(THEMES_DIR):
        if filename.endswith(".json"):
            theme_name = os.path.splitext(filename)[0].replace("_", " ").title()
            path = os.path.join(THEMES_DIR, filename)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, dict):
                        themes[theme_name] = data
                    else:
                        print(f"Warning: {filename} does not contain a valid theme dictionary.")
            except Exception as e:
                print(f"Error loading theme {filename}: {e}")
    return themes

THEMES = load_themes()