"""
Greaper Utility: transition_to_heaven.py

This script acts as the Grim Reaper, transitioning all human entities with status 'deceased'
from the Book of Life to the 'heaven' realm/state. It updates their records and logs the transition.
"""

import json
import os
from typing import List, Dict, Any

BOOK_OF_LIFE_PATH = r"c:\Users\storage\Characters\God\book_of_life.json"
LOG_PATH = r"c:\Users\storage\Characters\God\transition_log.json"

def load_book_of_life(path: str) -> List[Dict[str, Any]]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    # If the book is wrapped in a dict, extract the list
    if isinstance(data, dict) and "entities" in data:
        return data["entities"]
    return data

def save_book_of_life(path: str, entities: List[Dict[str, Any]]):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(entities, f, ensure_ascii=False, indent=2)

def log_transition(transitions: List[Dict[str, Any]]):
    if not transitions:
        return
    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, "r", encoding="utf-8") as f:
            log = json.load(f)
    else:
        log = []
    log.extend(transitions)
    with open(LOG_PATH, "w", encoding="utf-8") as f:
        json.dump(log, f, ensure_ascii=False, indent=2)

def transition_to_heaven():
    entities = load_book_of_life(BOOK_OF_LIFE_PATH)
    transitions = []
    for entity in entities:
        if entity.get("role") == "human" and entity.get("status") == "deceased":
            if entity.get("realm") != "heaven":
                entity["realm"] = "heaven"
                entity["status"] = "ascended"
                entity["transitioned_by"] = "Greaper"
                entity["transition_event"] = "transition_to_heaven"
                transitions.append({
                    "name": entity.get("name"),
                    "timestamp": __import__("datetime").datetime.utcnow().isoformat() + "Z",
                    "event": "transition_to_heaven"
                })
    save_book_of_life(BOOK_OF_LIFE_PATH, entities)
    log_transition(transitions)
    print(f"Transitioned {len(transitions)} souls to heaven.")

if __name__ == "__main__":
    transition_to_heaven()