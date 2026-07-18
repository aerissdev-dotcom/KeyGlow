import typer

from rich import print
from rich.table import Table
from rich.console import Console

from keyglow.storage import load_data, save_data, reset_data
from keyglow.monitor import start_monitor
from keyglow.map import show_map
from keyglow.export import export_json, export_csv, export_txt
from keyglow.jokes import get_joke
from pathlib import Path
from keyglow.logo import show_logo

def version_callback(value: bool):
    if value:
        print("KeyGlow v0.1.1")
        raise typer.Exit()

app = typer.Typer(
    name="keyglow",
    help="Privacy-first, useful and fun keyboard usage heatmap."
)

@app.callback(invoke_without_command=True)
def main(ctx: typer.Context, version: bool = typer.Option(None, "--version", "-v", callback=version_callback, is_eager=True, help="Show KeyGlow version.")):
    if ctx.invoked_subcommand is None:
        show_logo()
        print("\nRun 'keyglow --help' to see available commands.")
        raise typer.Exit()

console = Console()

def get_color(presses):

    if presses == 0:
        return "#4B5563"

    if presses < 10:
        return "#22C55E"

    if presses < 50:
        return "#166534"

    if presses < 200:
        return "#EAB308"

    if presses < 500:
        return "#F97316"

    return "#B91C1C"

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

    print("KeyGlow v0.1.1")



@app.command()
def privacy():
    """Explain KeyGlow Privacy Model."""

    print("""
[bold cyan]KeyGlow Privacy Model[/bold cyan]

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
    if not data:
        print("[bold yellow]No keyboard statistics available yet. [/bold yellow]")
        print("Run [bold cyan]keyglow monitor[/bold cyan] to start collecting data.")
        raise typer.Exit()

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

    def sort_key(item):
        key, presses = item
        is_letter = len(key) == 1 and key.isalpha()
        return(-presses, 0 if is_letter else 1, key)
    
    sorted_data = sorted(data.items(), key=sort_key)


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
def reset(force: bool = typer.Option(False, "--force", "-f", help="Skip confirmation and reset immediately.")):
    """Reset all KeyGlow data."""

    if not force:
        confirm = typer.confirm("Are you sure you want to delete all KeyGlow data?")
    
        if not confirm:
            print("[bold yellow]Reset cancelled.[/bold yellow]")
            raise typer.Exit()
        
    if reset_data():
        print("[bold green]KeyGlow data reset.[/bold green]")
    else:
        print("[bold yellow]No KeyGlow data found.[/bold yellow]")

@app.command()
def monitor(timeout: int = typer.Option(10, "--timeout", "-t", min = 0, help="Automatically stop monitoring after X minutes of inactivity (0 = disabled)")):
    """Start KeyGlow keyboard monitoring."""

    start_monitor(idle_timeout=timeout)

@app.command()
def map():
    """Show keyboard heatmap."""

    show_map()

@app.command()
def total():
    """Show total key presses."""

    data = load_data()

    total_presses = sum(
        data.values()
    )


    table = Table(
        title="KeyGlow Total Key Presses",
        border_style="#38BDF8"
    )


    table.add_column(
        "Statistic"
    )

    table.add_column(
        "Value",
        justify="right"
    )


    table.add_row(
        "Total Presses",
        f"[bold #38BDF8]{total_presses:,}[/bold #38BDF8]"
    )


    console.print(table)



@app.command()
def man():
    """Show the KeyGlow manual."""
    show_logo()

    print("""
[bold cyan]KeyGlow Manual[/bold cyan]


[bold red]NAME[/bold red]

  [bold yellow]KeyGlow[/bold yellow] - Privacy-first keyboard usage heatmap.


[bold red]USAGE[/bold red]

  [bold yellow]keyglow[/bold yellow] [COMMAND]
          

[bold red]COMMANDS[/bold red]

  [bold cyan]version[/bold cyan]       Show KeyGlow version.

  [bold cyan]privacy[/bold cyan]       Explain the privacy model.

  [bold cyan]monitor[/bold cyan]       Start keyboard monitoring.

  [bold cyan]stats[/bold cyan]         Show keyboard statistics.

  [bold cyan]map[/bold cyan]           Display the keyboard heatmap.

  [bold cyan]total[/bold cyan]         Show total recorded key presses.

  [bold cyan]export[/bold cyan]        Export collected statistics.

  [bold cyan]reset[/bold cyan]         Reset all collected data.

  [bold cyan]--help[/bold cyan]        Show command help.
          
  [bold cyan]joke[/bold cyan]          Show a random keyboard joke.
          
  [bold cyan]info[/bold cyan]          Show information about KeyGlow statistics, storage and configuration. 

  [bold cyan]logo[/bold cyan]          Show a logo of KeyGlow
[bold red]FILES[/bold red]

  [bold cyan]~/KeyGlow/[/bold cyan]     Local storage containing keyboard statistics.


[bold red]PRIVACY[/bold red]

  [bold italic magenta]Disclaimer:[/bold italic magenta]

  KeyGlow is not a keylogger.
  It only stores anonymous key frequency counters.
  It never records passwords, text, or key sequences.


[bold red]AUTHOR[/bold red]

  aeriss-dev


[bold red]GITHUB[/bold red]

  [link=https://github.com/aerissdev-dotcom]github.com/aerissdev-dotcom[/link]


[bold red]LICENSE[/bold red]

  MIT License


[bold red]VERSION[/bold red]

  0.1.1

""")



@app.command()
def export(
    format: str = typer.Argument(
        "json",
        help="Export format: json, csv or txt"
    )
):
    """Export KeyGlow statistics."""

    data = load_data()
    if not data:
        print("[bold yellow]Nothing to export.[/bold yellow]")
        raise typer.Exit()

    if format.lower() == "json":

        file = export_json()


    elif format.lower() == "csv":

        file = export_csv()


    elif format.lower() == "txt":

        file = export_txt()


    else:

        print(
            "[bold red]Unknown format.[/bold red] Use json, csv or txt."
        )

        raise typer.Exit()
    
    print(
        f"[bold cyan]Export completed:[/bold cyan] {file}"
    )

@app.command()
def joke():
    """Show a random keyboard joke."""
    print(f"""
[bold cyan]KeyGlow Joke[/bold cyan]
          
{get_joke()}
""")

@app.command()
def info():
    """Show KeyGlow information and statistics."""

    data = load_data()
    data_file = Path.home() / "KeyGlow" / "keyglow_data.json"
    export_folder = Path.home() / "KeyGlow" / "Exports"

    stored_keys = len(data)
    total_presses = sum(data.values())

    if data_file.exists():
        size_bytes = data_file.stat().st_size
        if size_bytes < 1024:
            database_size = f"{size_bytes} B"
        else:
            database_size = f"{size_bytes / 1024:.1f} KB"
    else:
        database_size = "0 B"
    
    table = Table(title = "KeyGlow Information", border_style="#38BDF8")
    table.add_column("Property")
    table.add_column("Value", justify="right")
    table.add_row("Version", "0.1.1")
    table.add_row("Stored keys", str(stored_keys))
    table.add_row("Total presses", f"{total_presses:,}")
    table.add_row("Database size", database_size)
    table.add_row("Export folder", str(export_folder))

    console.print(table)

@app.command()
def logo():
    """Show KeyGlow logo."""
    show_logo()


if __name__ == "__main__":
    app()

