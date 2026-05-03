import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SETTINGS_FILE  = os.path.join(BASE_DIR, "settings.json")
LEADERBOARD_FILE = os.path.join(BASE_DIR, "leaderboard.json")

DEFAULT_SETTINGS = {
    "sound":      True,
    "car_color":  "yellow",   # "yellow" | "red" | "blue" | "green" | "magenta" | "truqouise"
    "difficulty": "normal",    # "easy" | "normal" | "hard"
}


def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS.copy()
    with open(SETTINGS_FILE, "r") as f:
        data = json.load(f)
    for key, val in DEFAULT_SETTINGS.items():
        data.setdefault(key, val)
    return data

def save_settings(settings: dict):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=4)


def load_leaderboard():
    if not os.path.exists(LEADERBOARD_FILE):
        return []
    with open(LEADERBOARD_FILE, "r") as f:
        return json.load(f)

def save_score(name: str, score: int, distance: int, coins: int):
    board = load_leaderboard()
    board.append({
        "name":     name,
        "score":    score,
        "distance": distance,
        "coins":    coins,
    })
    board.sort(key=lambda x: x["score"], reverse=True)
    board = board[:10]
    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(board, f, indent=4)

def get_top_scores():
    return load_leaderboard() 