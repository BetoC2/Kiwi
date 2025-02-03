from commands import setup_info, add_class
from cover import generate_cover
from pathlib import Path
from rich import print
import typer, sys

app = typer.Typer()


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    id: str = typer.Option(None, "--id", "-i", help="ID de la clase"),
    title: str = typer.Option(None, "--title", "-t", help="Título del trabajo"),
):
    if ctx.invoked_subcommand is None:
        generate_cover(id, title)


@app.command()
def setup(
    path: Path = typer.Option(
        ...,
        "--path",
        "-p",
        exists=True,
        file_okay=False,
        dir_okay=True,
        readable=True,
        help="Ruta del directorio donde guardas tus clases.",
    ),
):
    setup_info(path)


@app.command()
def add():
    add_class()


if __name__ == "__main__":
    app()
