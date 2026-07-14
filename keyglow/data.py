import string


KEY_STATS = {
    key: 0 for key in string.ascii_uppercase
}


KEY_STATS.update({

    # Numbers
    "0": 0,
    "1": 0,
    "2": 0,
    "3": 0,
    "4": 0,
    "5": 0,
    "6": 0,
    "7": 0,
    "8": 0,
    "9": 0,


    # Symbols
    "`": 0,
    "-": 0,
    "=": 0,
    "[": 0,
    "]": 0,
    "\\": 0,
    ";": 0,
    "'": 0,
    ",": 0,
    ".": 0,
    "/": 0,


    # Special keys
    "SPACE": 0,
    "ENTER": 0,
    "BACKSPACE": 0,
    "TAB": 0,
    "CAPSLOCK": 0,


    # Modifiers
    "SHIFT": 0,
    "CTRL": 0,
    "ALT": 0,
    "SYSTEM": 0,


    # Navigation
    "UP": 0,
    "DOWN": 0,
    "LEFT": 0,
    "RIGHT": 0,


    # Function keys
    "F1": 0,
    "F2": 0,
    "F3": 0,
    "F4": 0,
    "F5": 0,
    "F6": 0,
    "F7": 0,
    "F8": 0,
    "F9": 0,
    "F10": 0,
    "F11": 0,
    "F12": 0,
})