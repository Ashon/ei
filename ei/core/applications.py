import typer

from ei.views.cli import ami
from ei.views.cli import ec2
from ei.views.cli import elasticache
from ei.views.cli import vpc


APPS = [
    ec2.Ec2CliApp,
    ami.AmiCliApp,
    vpc.VpcCliApp,
    elasticache.ReplicationGroupCliApp,
    elasticache.CacheClusterCliApp,
]


def create_application() -> typer.Typer:
    cli = typer.Typer(help='A[ei] - AWS CLI for humans.')

    for app in APPS:
        obj = app()
        cli.add_typer(obj.typer())

    return cli
