import typer

from rich import print
from rich.table import Table
from rich.console import Console

from keyglow.storage import (
    load_data,
    increment_key,
    reset_data
)

from keyglow.monitor import start_monitor
from keyglow.map import show_map


app = typer.Typer(
    name="keyglow",
    help="Privacy-first, useful and fun keyboard usage heatmap."
)


console = Console()


def get_color(presses):

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



def get_bar(presses):

    if presses == 0:
        return ""

    return "█" * max(
        1,
        min(
            presses // 10,
            20
        )
    )


@app.command()
def version():
    """Show KeyGlow version."""

    print("KeyGlow v0.1.0")



@app.command()
def privacy():
    """Explain KeyGlow Privacy Model."""

    print("""
[bold]KeyGlow Privacy Model[/bold]

Collected:
    [green][+][/green] Key frequency counters

Never Collected:
    [red][-][/red] Typed text
    [red][-][/red] Passwords
    [red][-][/red] Key sequences
    [red][-][/red] Clipboard data

[dim]All data stays locally on your device.[/dim]
""")



@app.command()
def stats():
    """Show keyboard statistics."""

    data = load_data()

    table = Table(
        title="KeyGlow Keyboard Statistics",
        border_style="#38BDF8"
    )


    table.add_column(
        "Key",
        justify="center"
    )

    table.add_column(
        "Presses",
        justify="right"
    )

    table.add_column(
        "Usage"
    )


    sorted_data = sorted(
        data.items(),
        key=lambda item: item[1],
        reverse=True
    )


    for key, presses in sorted_data:

        color = get_color(presses)

        bar = get_bar(presses)


        table.add_row(
            f"[{color}]{key}[/{color}]",
            f"[{color}]{presses}[/{color}]",
            f"[{color}]{bar}[/{color}]"
        )


    console.print(table)



@app.command()
def press(key: str):
    """Simulate a key press."""

    key = key.upper()

    increment_key(key)



@app.command()
def reset():
    """Reset all KeyGlow data."""

    reset_data()

    print(
        "KeyGlow data reset."
    )



@app.command()
def monitor():
    """Start KeyGlow keyboard monitoring."""

    start_monitor()



@app.command()
def map():
    """Show keyboard heatmap."""

    show_map()

@app.command()
def total():
    """Show total key presses."""

    data = load_data()
    total_presses = sum(data.values())

    table = Table(title = "KeyGlow Total Key Presses", border_style="#38BDF8")
    table.add_column("Statistic")
    table.add_column("Value", justify="right")

    table.add_row("Total Presses", f"[bold #38BDF8]{total_presses:,}[/bold #38BDF8]")

    console.print(table)

if __name__ == "__main__":
    app()