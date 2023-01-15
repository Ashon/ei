from typing import Type

from ei.core.cli import BaseCliApp
from ei.core.service import BaseAwsService
from ei.core.fields import Field
from ei.core.fields import IDField
from ei.core.fields import BooleanField
from ei.core.fields import TagField
from ei.services.aws.ami import AwsAmiService


class AmiCliApp(BaseCliApp):
    name: str = 'ami'
    description: str = 'EC2 AMI'

    service_cls: Type[BaseAwsService] = AwsAmiService

    short_fields = (
        Field('Region'),
        Field('Account'),
        IDField('ImageId'),
        Field('Name'),
        BooleanField('Public'),
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
