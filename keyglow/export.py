import json
import csv

from pathlib import Path
from datetime import datetime

from keyglow.storage import load_data


EXPORT_DIR = Path.home() / "KeyGlow" / "Exports"

def ensure_export_dir():
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)

def create_export_path(extension):
    """
    Creates export folder and filename with timestamp.
    """

    EXPORT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    timestamp = datetime.now().strftime(
        "%Y-%m-%d_%H-%M-%S"
    )

    return EXPORT_DIR / (
        f"keyglow_export_{timestamp}.{extension}"
    )



def export_json():
    ensure_export_dir()
    data = load_data()

    file = create_export_path("json")


    with file.open(
        "w",
        encoding="UTF-8"
    ) as f:

        json.dump(
            data,
            f,
            indent=4,
            ensure_ascii=False
        )


    return file



def export_csv():
    ensure_export_dir()
    data = load_data()

    file = create_export_path("csv")


    with file.open(
        "w",
        newline="",
        encoding="UTF-8"
    ) as f:

        writer = csv.writer(f)

        writer.writerow(
            [
                "Key",
                "Presses"
            ]
        )


        for key, presses in data.items():

            writer.writerow(
                [
                    key,
                    presses
                ]
            )


    return file



def export_txt():
    ensure_export_dir()
    data = load_data()

    file = create_export_path("txt")


    total = sum(data.values())


    sorted_data = sorted(
        data.items(),
        key=lambda x: x[1],
        reverse=True
    )


    with file.open(
        "w",
        encoding="UTF-8"
    ) as f:

        f.write(
            "==============================\n"
        )

        f.write(
            "KeyGlow Export\n"
        )

        f.write(
            "==============================\n\n"
        )


        f.write(
            f"Total key presses:\n{total}\n\n"
        )


        f.write(
            "Keyboard statistics:\n\n"
        )


        for key, presses in sorted_data:

            f.write(
                f"{key:<12}{presses}\n"
            )


        f.write(
            "\nPrivacy:\n\n"
        )

        f.write(
            "KeyGlow stores only key frequency counters.\n"
        )

        f.write(
            "No typed text, passwords or key sequences are recorded.\n"
        )


    return file