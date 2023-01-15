import typing

import typer

from ei.core.cli import CliGroup
from ei.views.cli import ec2
from ei.views.cli import elasticache
from ei.views.cli import rds


if typing.TYPE_CHECKING:
    from ei.core.cli import Typeable  # noqa: F401


APPS = [
    ec2.group,
    elasticache.group,
    rds.group,
]  # type: list[Typeable]


def create_application() -> typer.Typer:
    cli = CliGroup(
        name='ei',
        description=(
            'A[bold green](ei)[/bold green]'
            ' - AWS CLI for humans.'
        ),
        apps=APPS
    )

    return cli.typer()
