import typer

from ei.cli import ami
from ei.cli import ec2
from ei.cli import vpc


APPS = [
    ec2.Ec2CliApp,
    ami.AmiCliApp,
    vpc.VpcCliApp
]


def main():
    cli = typer.Typer()

    for app in APPS:
        obj = app()
        cli.add_typer(obj.typer())

    return cli


cli = main()
