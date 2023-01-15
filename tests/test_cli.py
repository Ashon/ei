import typing

from ei.core.cli import create_application
from ei.views.cli import ec2
from ei.views.cli import elasticache
from ei.views.cli import rds


if typing.TYPE_CHECKING:
    from ei.core.cli import Typeable  # noqa: F401


def test_create_application() -> None:
    apps = [
        ec2.group,
        elasticache.group,
        rds.group
    ]  # type: typing.List[Typeable]

    create_application(apps)


def test_main() -> None:
    from ei.main import cli  # noqa: F401
