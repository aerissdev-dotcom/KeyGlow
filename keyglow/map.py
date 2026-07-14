from rich import print
from keyglow.keyboard import KEYBOARD_LAYOUT
from keyglow.storage import load_data

KEY_SIZES = {
    "SPACE": 20,
    "BACKSPACE": 12,
    "ENTER": 10,
    "CAPSLOCK": 10,
    "SHIFT": 10,
    "TAB": 8,
    "CTRL": 8,
    "ALT": 8,
    "SYS": 8,
}

def get_width(key):
    if key in KEY_SIZES:
        return KEY_SIZES[key]

    return max(len(key) + 2, 7)


def get_color(presses):
    """
    Heatmap color scale.
    """

    if presses == 0:
        return "#4B5563"  # dark gray

    if presses < 10:
        return "#22C55E"  # green
    
    if presses < 50:
        return "#166534"  # dark green

    if presses < 200:
        return "#EAB308"  # yellow

    if presses < 500:
        return "#F97316"  # orange

    return "#B91C1C"      # dark red


def get_bar(presses, width):
    """
    Creates usage bar.
    """

    if presses == 0:
        return ""

    amount = max(
        1,
        min(
            presses // 10,
            width - 2
        )
    )

    return "█" * amount


def make_key(key, presses):
    """
    Creates one ASCII key.
    """

    width = get_width(key)

    color = get_color(presses)

    bar = get_bar(
        presses,
        width
    )

    top = (
        f"[{color}]+"
        f"{'-' * width}"
        f"+[/{color}]"
    )

    middle = (
        f"[{color}]|"
        f"{key.center(width)}"
        f"|[/{color}]"
    )

    usage = (
        f"[{color}]|"
        f"{bar.center(width)}"
        f"|[/{color}]"
    )

    bottom = (
        f"[{color}]+"
        f"{'-' * width}"
        f"+[/{color}]"
    )

    return [
        top,
        middle,
        usage,
        bottom
    ]


def show_map():

    data = load_data()

    print("\n[bold #38BDF8]KeyGlow Keyboard Map[/bold #38BDF8]\n")

    for row in KEYBOARD_LAYOUT:

        rendered_keys = []

        for key in row:
            rendered_keys.append(
                make_key(
                    key,
                    data.get(key, 0)
                )
            )

        for line in range(4):
            print(
                "   ".join(
                    key[line]
                    for key in rendered_keys
                )
            )

        print()