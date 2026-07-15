import time
import threading

from pynput import keyboard
from pynput import mouse

from keyglow.storage import load_data, save_data



def normalize_key(key):

    try:
        if key.char:
            return key.char.upper()

    except AttributeError:
        pass


    special_keys = {
        keyboard.Key.space: "SPACE",
        keyboard.Key.enter: "ENTER",
        keyboard.Key.tab: "TAB",
        keyboard.Key.backspace: "BACKSPACE",
        keyboard.Key.caps_lock: "CAPSLOCK",
        keyboard.Key.esc: "ESC",
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



def start_monitor(idle_timeout=10):

    print("KeyGlow monitor started...")
    print("Press CTRL+C to stop.")


    data = load_data()

    last_activity = time.time()
    running = True



    def autosave():

        while running:

            time.sleep(5)
            save_data(data)



    threading.Thread(
        target=autosave,
        daemon=True
    ).start()



    def inactivity_checker():

        nonlocal running, last_activity


        if idle_timeout == 0:
            return


        while running:

            time.sleep(1)


            inactivity_time = time.time() - last_activity


            if inactivity_time >= idle_timeout * 60:

                print(
                    f"\nNo activity detected for {idle_timeout} minute(s). "
                    "KeyGlow monitor stopped."
                )


                running = False

                save_data(data)

                break



    threading.Thread(
        target=inactivity_checker,
        daemon=True
    ).start()



    def on_press(key):

        nonlocal last_activity


        last_activity = time.time()


        normalized = normalize_key(key)


        if normalized:

            if normalized not in data:
                data[normalized] = 0


            data[normalized] += 1



    def on_mouse_activity(*args):

        nonlocal last_activity

        last_activity = time.time()



    keyboard_listener = keyboard.Listener(
        on_press=on_press
    )


    mouse_listener = mouse.Listener(
        on_move=on_mouse_activity,
        on_click=on_mouse_activity,
        on_scroll=on_mouse_activity
    )



    keyboard_listener.start()
    mouse_listener.start()



    try:

        while running:
            time.sleep(1)


    except KeyboardInterrupt:
        pass


    finally:

        running = False

        keyboard_listener.stop()
        mouse_listener.stop()

        save_data(data)