#! /usr/bin/env -S uv run --script
import typer

from cli_commands.main import app as cli_app

app = typer.Typer(no_args_is_help=True)
app.add_typer(cli_app)


@app.callback()
def callback():
    """Простой CLI manager"""
    pass


if __name__ == "__main__":
    app()
