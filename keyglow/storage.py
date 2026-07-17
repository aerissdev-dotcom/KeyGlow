import json
from pathlib import Path
import typer

KEYGLOW_DIR = Path.home() / "KeyGlow"

DATA_FILE = KEYGLOW_DIR / "keyglow_data.json"

def ensure_keyglow_dir():
        KEYGLOW_DIR.mkdir(parents=True, exist_ok=True)

def save_data(data):
    ensure_keyglow_dir()
    try:
        with open(DATA_FILE, "w", encoding="UTF-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
    except OSError:
        print("Failed to save KeyGlow database.")
        raise typer.Exit(code=1)
        
def load_data():

    if not DATA_FILE.exists():
        return {}

    try:
        with open(DATA_FILE, "r", encoding="UTF-8") as file:
            data = json.load(file)
            if not isinstance(data, dict):
                print("Invalid KeyGlow database format.")
                raise typer.Exit(code=1)
            
            for key, value in data.items():

                if not isinstance(key, str):
                    print("Invalid KeyGlow database format.")
                    raise typer.Exit(code=1)
                
                if not isinstance(value, int):
                    print("Invalid KeyGlow database format.")
                    raise typer.Exit(code=1)

                if value < 0:
                    print("Invalid KeyGlow database format.")
                    raise typer.Exit(code=1)

            return data
    except json.JSONDecodeError:
        print("KeyGlow database is corrupted.")
        raise typer.Exit(code=1)
    
def reset_data():
    if not DATA_FILE.exists():
        return False
    DATA_FILE.unlink()

    return True
