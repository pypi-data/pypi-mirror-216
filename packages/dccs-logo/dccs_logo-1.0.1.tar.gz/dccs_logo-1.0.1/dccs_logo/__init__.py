import os

try:
    from rich import print
except ImportError:
    os.system("pip install rich")


def logo(a, t, v, g):
    logo = f"""
[bold red]×_×[/bold red][bold yellow] d8888b.  .o88b.  .o88b. .d8888.
[bold green][T][/bold green][bold yellow] 88  `8D d8P  Y8 d8P  Y8 88'  YP
[bold blue][E][/bold blue][bold yellow] 88   88 8P      8P      `8bo.
[bold magenta][A][/bold magenta][bold yellow] 88   88 8b      8b        `Y8b.
[bold cyan][M][/bold cyan][bold yellow] 88  .8D Y8b  d8 Y8b  d8 db   8D
[bold red]×_×[/bold red][bold yellow] Y8888D'  `Y88P'  `Y88P' `8888Y'
[bold white]
    \t    [bold cyan] [ MURSALIN × SAIMUN ] [/bold cyan]
    \t[bold white]┌━━━━━━━━━━━━━━━━━━━━━━━━━━┑
    \t┃ [bold white]Author :[/bold white] {a}┃
    \t┃ [bold white]Tools  :[/bold white] {t}┃
    \t┃ [bold white]Version:[/bold white] {v}┃
    \t┃ [bold white]Github :[/bold white] {g}┃
    \t└━━━━━━━━━━━━━━━━━━━━━━━━━━┘
[bold white]
"""
    return logo


def logo2(a, t, v, g):
    logo = f"""
    [bold red]×_×[/bold red][bold yellow] d8888b.  .o88b.  .o88b. .d8888.
    [bold green][T][/bold green][bold yellow] 88  `8D d8P  Y8 d8P  Y8 88'  YP
    [bold blue][E][/bold blue][bold yellow] 88   88 8P      8P      `8bo.
    [bold magenta][A][/bold magenta][bold yellow] 88   88 8b      8b        `Y8b.
    [bold cyan][M][/bold cyan][bold yellow] 88  .8D Y8b  d8 Y8b  d8 db   8D
    [bold red]×_×[/bold red][bold yellow] Y8888D'  `Y88P'  `Y88P' `8888Y'
    [bold white]
 \t       [bold cyan] [ MURSALIN × SAIMUN ] [/bold cyan]
\t    [bold white]┌━━━━━━━━━━━━━━━━━━━━━━━━━━┑
\t    ┃ [bold white]Author :[/bold white] {a}┃
\t    ┃ [bold white]Tools  :[/bold white] {t}┃
\t    ┃ [bold white]Version:[/bold white] {v}┃
\t    ┃ [bold white]Github :[/bold white] {g}┃
\t    └━━━━━━━━━━━━━━━━━━━━━━━━━━┘
    [bold white]
    """
    return logo
    