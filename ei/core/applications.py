import typer

from ei.core.cli import Typeable
from ei.views.cli import ec2
from ei.views.cli import elasticache
from ei.views.cli import rds


APPS = [
    ec2.group,
    elasticache.group,
    rds.group,
]


def create_application() -> typer.Typer:
    cli = typer.Typer(
        help=(
            'A[bold green](ei)[/bold green]'
            ' - AWS CLI for humans.'
        ),
        rich_markup_mode='rich'
    )

    for app in APPS:
        assert isinstance(app, Typeable)
        cli.add_typer(app.typer())

    return cli
