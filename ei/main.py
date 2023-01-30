import typing

from ei.core.cli import create_application
from ei.views.cli import ec2
from ei.views.cli import elasticache
from ei.views.cli import rds
from ei.views.cli import s3
from ei.views.cli import elb


if typing.TYPE_CHECKING:
    from ei.core.cli import Typeable  # noqa: F401


APPS = [
    ec2.group,
    elasticache.group,
    rds.group,
    s3.group,
    elb.group
]  # type: typing.List[Typeable]


cli = create_application(APPS)
