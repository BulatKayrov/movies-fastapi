import typer
from rich import print
from rich.markdown import Markdown

from api.v1.movie.auth.service import redis_tokens_helper

app = typer.Typer(no_args_is_help=True, rich_markup_mode="rich")


@app.command(help="Check you TOKEN in REDIS DATABASE")
def check_token(token: str = typer.Argument()):
    if redis_tokens_helper.token_exists(token):
        print(f"Token [green][italic]{token} exists[/italic][/green]")
    else:
        print("Token [red][bold]does not exist[/bold][/red]")


@app.command(help="Get all tokens")
def list():
    print(Markdown("## Tokens"))
    print("\n".join(redis_tokens_helper.get_tokens()))
