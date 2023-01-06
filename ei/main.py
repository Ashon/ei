import typer
from ei.cli import ec2
from ei.cli import vpc


cli = typer.Typer()
cli.add_typer(ec2.app)
cli.add_typer(vpc.app)
