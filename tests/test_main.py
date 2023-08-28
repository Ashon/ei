import typing

from ei.core.cli import create_application
from ei.views.cli import ec2
from ei.views.cli import elasticache
from ei.views.cli import rds
from ei.views.cli import s3
from ei.views.cli import elb
from ei.services.aws.ec2 import AwsEc2VpcService
from ei.services.aws.ec2 import AwsEc2SubnetService
from ei.services.aws.ec2 import AwsEc2InstanceService
from ei.services.aws.ec2 import AwsEc2AmiService
from ei.services.aws.ec2 import AwsEc2RouteTableService
from ei.services.aws.ec2 import AwsEc2TransitGatewayService
from ei.services.aws.ec2 import AwsEc2SecurityGroupService
from ei.services.aws.elasticache import AwsElasticacheReplicationGroupService
from ei.services.aws.elasticache import AwsElasticacheCacheClusterService
from ei.services.aws.elasticache import AwsElasticacheEventService
from ei.services.aws.elb import AwsElbLoadbalancerService
from ei.services.aws.elb import AwsElbListenerService
from ei.services.aws.elb import AwsElbTargetGroupService
from ei.services.aws.rds import AwsRdsInstanceService
from ei.services.aws.s3 import AwsS3BucketService


if typing.TYPE_CHECKING:
    from ei.core.cli import Typeable  # noqa: F401


def test_create_application() -> None:
    service_classes = [
        AwsEc2VpcService,
        AwsEc2SubnetService,
        AwsEc2InstanceService,
        AwsEc2AmiService,
        AwsEc2RouteTableService,
        AwsEc2TransitGatewayService,
        AwsEc2SecurityGroupService,
        AwsElasticacheReplicationGroupService,
        AwsElasticacheCacheClusterService,
        AwsElasticacheEventService,
        AwsElbLoadbalancerService,
        AwsElbListenerService,
        AwsElbTargetGroupService,
        AwsRdsInstanceService,
        AwsS3BucketService
    ]

    apps = [
        ec2.group,
        elasticache.group,
        rds.group,
        s3.group,
        elb.group
    ]  # type: typing.List[Typeable]

    create_application(apps, service_classes)


def test_main() -> None:
    from ei.main import cli  # noqa: F401
