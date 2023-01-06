from ei.core.cli import BaseCliApp
from ei.core.fields import Field
from ei.core.fields import TagField
from ei.aws.ami import AwsAmiService


class AmiCliApp(BaseCliApp):
    name: str = 'ami'
    description: str = 'EC2 AMI'

    service_cls = AwsAmiService

    short_fields = (
        Field('Region'),
        Field('Account'),
        Field('ImageId'),
        Field('Name'),
        Field('Public'),
        Field('State'),
        Field('CreationDate'),
    )

    long_fields = (
        Field('Description'),
        Field('ImageType'),
        Field('Hypervisor'),
        Field('Architecture'),
        Field('PlatformDetails'),
        TagField('Tags')
    )

    detail_fields = (
        Field('UsageOperation'),
        Field('RootDeviceName'),
        Field('RootDeviceType'),
        Field('EnaSupport'),
        Field('SriovNetSupport'),
        Field('VirtualizationType'),
        Field('DeprecationTime'),
        Field('ImageLocation'),
        Field('OwnerId'),
        Field('BlockDeviceMappings'),
        Field('ImageOwnerAlias'),
    )
