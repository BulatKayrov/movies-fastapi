import typer

from .colors import colors_app

app = typer.Typer(
    no_args_is_help=True,
)
app.add_typer(colors_app)
