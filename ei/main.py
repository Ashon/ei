import typer
from ei.cli import ec2
from ei.cli import vpc


APPS = [
    ec2.app,
    vpc.app
]


def main():
    cli = typer.Typer()

    for app in APPS:
        cli.add_typer(app)

    return cli


cli = main()
