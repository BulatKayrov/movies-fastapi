import typer
from rich import print

colors_app = typer.Typer(no_args_is_help=True, rich_markup_mode="rich")


@colors_app.command(
    help="Команда которая просто выводит текст либо красного либо зеленого цвета. Достаточно в качестве аргумента передать название на англ.языке"
)
def colorize(color: str) -> None:
    if color == "red":
        print("[red]Вы выбрали красный цвет[/red]")
    if color == "green":
        print("[green]Вы выбрали зеленый цвет[/green]")
