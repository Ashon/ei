from ei.cli.base import BaseCliApp
from ei.aws.vpc import AwsVpcService
from ei.core.field_serializers import serialize_tags
from ei.core.field_serializers import serialize_dict_list


class VpcCliApp(BaseCliApp):
    name: str = 'vpc'
    service_cls = AwsVpcService

    short_fields = (
        ('Region', str),
        ('VpcId', str),
        ('OwnerId', str),
        ('InstanceTenancy', str),
        ('IsDefault', str),
        ('State', str),
        ('DhcpOptionsId', str),
        ('CidrBlock', str)
    )

    long_fields = (
        ('CidrBlockAssociationSet', serialize_dict_list),
        ('Tags', serialize_tags)
    )


app = VpcCliApp().typer()
