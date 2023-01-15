import typing

from ei.core.cli import create_application
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


cli = create_application(APPS)
