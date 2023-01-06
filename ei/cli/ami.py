from ei.cli.base import BaseCliApp
from ei.aws.ami import AwsAmiService
from ei.core.field_serializers import serialize_tags
# from ei.core.field_serializers import serialize_dict_list


class AmiCliApp(BaseCliApp):
    name: str = 'ami'
    description: str = 'EC2 AMI'

    service_cls = AwsAmiService

    short_fields = (
        ('Region', str),
        ('Account', str),
        ('ImageId', str),
        ('Name', str),
        ('Public', str),
        ('State', str),
        ('CreationDate', str),
    )

    long_fields = (
        ('Description', str),
        ('ImageType', str),
        ('Hypervisor', str),
        ('Architecture', str),
        ('PlatformDetails', str),
        ('Tags', serialize_tags)
    )

    detail_fields = (
        ('UsageOperation', str),
        ('RootDeviceName', str),
        ('RootDeviceType', str),
        ('EnaSupport', str),
        ('SriovNetSupport', str),
        ('VirtualizationType', str),
        ('DeprecationTime', str),
        ('ImageLocation', str),
        ('OwnerId', str),
        ('BlockDeviceMappings', str),
        ('ImageOwnerAlias', str),
    )
