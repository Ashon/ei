import typer

from ei.cli import ami
from ei.cli import ec2
from ei.cli import elasticache
from ei.cli import vpc


APPS = [
    ec2.Ec2CliApp,
    ami.AmiCliApp,
    vpc.VpcCliApp,
    elasticache.ReplicationGroupCliApp,
    elasticache.CacheClusterCliApp,
]


def create_application():
    cli = typer.Typer()

    for app in APPS:
        obj = app()
        cli.add_typer(obj.typer())

    return cli


__all__ = ['create_application']
