from ei.cli._base import BaseCliApp
from ei.aws.vpc import AwsVpcService
from ei.core.field_serializers import to_string
from ei.core.field_serializers import serialize_tags
from ei.core.field_serializers import serialize_dict_list


class VpcCliApp(BaseCliApp):
    name: str = 'vpc'
    description: str = 'EC2 VPC'

    service_cls = AwsVpcService

    short_fields = (
        ('Region', to_string),
        ('VpcId', to_string),
        ('OwnerId', to_string),
        ('InstanceTenancy', to_string),
        ('IsDefault', to_string),
        ('State', to_string),
        ('DhcpOptionsId', to_string),
        ('CidrBlock', to_string)
    )

    long_fields = (
        ('CidrBlockAssociationSet', serialize_dict_list),
        ('Tags', serialize_tags)
    )
