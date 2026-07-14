import json
from pathlib import Path


DATA_FILE = Path("keyglow_data.json")


def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)


def load_data():
    if not DATA_FILE.exists():
        return {}

    with open(DATA_FILE, "r") as file:
        return json.load(file)


def increment_key(key):
    data = load_data()

    if key in data:
        data[key] += 1
    else:
        data[key] = 1

    save_data(data)

def reset_data():
    if DATA_FILE.exists():
        DATA_FILE.unlink()
        