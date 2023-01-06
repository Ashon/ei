import typer

from ei.cli import APPS


def main():
    cli = typer.Typer()

    for app in APPS:
        obj = app()
        cli.add_typer(obj.typer())

    return cli


cli = main()
