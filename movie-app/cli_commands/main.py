import typer

from .colors import colors_app
from .tokens import app as tokens_app

app = typer.Typer(
    no_args_is_help=True,
)
app.add_typer(colors_app)
app.add_typer(tokens_app)
