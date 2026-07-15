import json
from pathlib import Path


DATA_FILE = Path("keyglow_data.json")


def save_data(data):
    with open(
        DATA_FILE,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False
        )


def load_data():

    if not DATA_FILE.exists():
        return {}

    with open(
        DATA_FILE,
        "r",
        encoding="utf-8"
    ) as file:
        return json.load(file)



def reset_data():

    if DATA_FILE.exists():
        DATA_FILE.unlink()