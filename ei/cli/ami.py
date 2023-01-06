from ei.cli._base import BaseCliApp
from ei.aws.ami import AwsAmiService
from ei.core.field_serializers import to_string
from ei.core.field_serializers import serialize_tags
# from ei.core.field_serializers import serialize_dict_list


class AmiCliApp(BaseCliApp):
    name: str = 'ami'
    description: str = 'EC2 AMI'

    service_cls = AwsAmiService

    short_fields = (
        ('Region', to_string),
        ('Account', to_string),
        ('ImageId', to_string),
        ('Name', to_string),
        ('Public', to_string),
        ('State', to_string),
        ('CreationDate', to_string),
    )

    long_fields = (
        ('Description', to_string),
        ('ImageType', to_string),
        ('Hypervisor', to_string),
        ('Architecture', to_string),
        ('PlatformDetails', to_string),
        ('Tags', serialize_tags)
    )

    detail_fields = (
        ('UsageOperation', to_string),
        ('RootDeviceName', to_string),
        ('RootDeviceType', to_string),
        ('EnaSupport', to_string),
        ('SriovNetSupport', to_string),
        ('VirtualizationType', to_string),
        ('DeprecationTime', to_string),
        ('ImageLocation', to_string),
        ('OwnerId', to_string),
        ('BlockDeviceMappings', to_string),
        ('ImageOwnerAlias', to_string),
    )
