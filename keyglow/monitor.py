from pynput import keyboard
from keyglow.storage import increment_key


def normalize_key(key):
    try:
        return key.char.upper()

    except AttributeError:

        special_keys = {
            keyboard.Key.space: "SPACE",
            keyboard.Key.enter: "ENTER",
            keyboard.Key.tab: "TAB",
            keyboard.Key.backspace: "BACKSPACE",
            keyboard.Key.caps_lock: "CAPSLOCK",
        }


        for key_name, label in {
            "shift": "SHIFT",
            "shift_l": "SHIFT",
            "shift_r": "SHIFT",

            "ctrl": "CTRL",
            "ctrl_l": "CTRL",
            "ctrl_r": "CTRL",

            "alt": "ALT",
            "alt_l": "ALT",
            "alt_r": "ALT",

            "cmd": "SYSTEM",
            "cmd_l": "SYSTEM",
            "cmd_r": "SYSTEM",

            "up": "UP",
            "down": "DOWN",
            "left": "LEFT",
            "right": "RIGHT",

        }.items():

            if hasattr(keyboard.Key, key_name):
                special_keys[getattr(keyboard.Key, key_name)] = label


        return special_keys.get(key)


def start_monitor():

    print("KeyGlow monitor started...")
    print("Press CTRL+C to stop.")


    def on_press(key):

        normalized = normalize_key(key)

        if normalized:
            increment_key(normalized)
            print(f"{normalized} + 1")


    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()