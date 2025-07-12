import typer
from rich import print
from rich.markdown import Markdown

from api.v1.movie.service import redis_tokens_helper

app = typer.Typer(no_args_is_help=True, rich_markup_mode="rich")


@app.command(help="Check you TOKEN in REDIS DATABASE")
def check_token(token: str = typer.Argument()) -> None:
    if redis_tokens_helper.token_exists(token):
        print(f"Token [green][italic]{token} exists[/italic][/green]")
    else:
        print("Token [red][bold]does not exist[/bold][/red]")


@app.command(help="Get all tokens")
def list() -> None:
    print(Markdown("## Tokens"))
    print("\n".join(redis_tokens_helper.get_tokens()))


@app.command(help="Генерация нового токена и сохранение его")
def create() -> None:
    print(redis_tokens_helper.create())


@app.command(help="Добавление нового токена в БД")
def add(
    token: str = typer.Argument(help="ТОКЕН который необходимо добавить в БД"),
) -> None:
    redis_tokens_helper.add_token(token)
    print(f"{token} saved")


@app.command(help="Удаление токена из БД")
def delete(
    token: str = typer.Argument(help="ТОКЕН который необходимо удалить"),
) -> None:
    redis_tokens_helper.delete_token(token)
    print(f"{token} deleted")
