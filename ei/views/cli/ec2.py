from typing import Type

from ei.core.cli import BaseCliApp
from ei.core.service import BaseAwsService
from ei.core.fields import Field
from ei.core.fields import IDField
from ei.core.fields import TagField
from ei.core.fields import DictField
from ei.core.fields import extract_from_tag
from ei.services.aws.ec2 import AwsEc2Service


class Ec2CliApp(BaseCliApp):
    name: str = 'ec2'
    description: str = 'EC2 instance'

    service_cls: Type[BaseAwsService] = AwsEc2Service

    short_fields = (
        Field('Region'),
        Field('Account'),
        IDField('InstanceId'),
        Field('Name', serializer=extract_from_tag('Name')),
        Field('ImageId'),
        Field('InstanceType'),
        Field('PrivateIpAddress'),
        Field('State', serializer=lambda record, raw_value: raw_value['Name']),
        Field('VpcId'),
    )

    long_fields = (
        Field('SubnetId'),
        Field('Hypervisor'),
        Field('Architecture'),
        TagField('Tags')
    )

    detail_fields = (
        Field('AmiLaunchIndex'),
        Field('LaunchTime'),
        Field('PrivateDnsName'),
        Field('ProductCodes'),
        Field('PublicDnsName'),
        Field('StateTransitionReason'),
        Field('ClientToken'),
        Field('EbsOptimized'),
        Field('EnaSupport'),
        DictField('Placement'),
        DictField('BlockDeviceMappings'),
        DictField('MaintenanceOptions'),
        DictField('Monitoring'),
        DictField('IamInstanceProfile'),
        DictField('NetworkInterfaces'),
        Field('RootDeviceName'),
        Field('RootDeviceType'),
        DictField('SecurityGroups'),
        Field('SourceDestCheck'),
        Field('VirtualizationType'),
        DictField('CpuOptions'),
        DictField('CapacityReservationSpecification'),
        DictField('HibernationOptions'),
        DictField('MetadataOptions'),
        DictField('EnclaveOptions'),
        Field('PlatformDetails'),
        Field('UsageOperation'),
        Field('UsageOperationUpdateTime'),
        DictField('PrivateDnsNameOptions'),
    )
