from typing import Type

from ei.core.cli import BaseCliApp
from ei.core.cli import CliGroup
from ei.core.service import BaseAwsService
from ei.core.fields import Field
from ei.core.fields import IDField
from ei.core.fields import BooleanField
from ei.core.fields import TagField
from ei.core.fields import DictField
from ei.core.fields import extract_from_tag
from ei.services.aws.ec2 import AwsEc2VpcService
from ei.services.aws.ec2 import AwsEc2SubnetService
from ei.services.aws.ec2 import AwsEc2InstanceService
from ei.services.aws.ec2 import AwsEc2AmiService


group = CliGroup(name='ec2', description='AWS EC2')


@group.app
class Ec2VpcCli(BaseCliApp):
    name: str = 'vpc'
    description: str = 'EC2 VPC'

    service_cls = AwsEc2VpcService

    short_fields = (
        Field('Region'),
        Field('Account'),
        IDField('VpcId'),
        Field('Name', serializer=extract_from_tag('Name')),
        Field('InstanceTenancy'),
        BooleanField('IsDefault'),
        Field('State'),
        Field('DhcpOptionsId'),
        Field('CidrBlock')
    )

    long_fields = (
        DictField('CidrBlockAssociationSet'),
        TagField('Tags')
    )


@group.app
class Ec2SubnetCli(BaseCliApp):
    name: str = 'subnet'
    description: str = 'EC2 Subnet'
    service_cls = AwsEc2SubnetService

    short_fields = (
        Field('Region'),
        Field('Account'),
        IDField('SubnetId'),
        Field('Name', serializer=extract_from_tag('Name')),
        Field('CidrBlock'),
        Field('AvailableIpAddressCount'),
        BooleanField('DefaultForAz'),
        BooleanField('MapPublicIpOnLaunch'),
        Field('State'),
        Field('VpcId'),
    )

    long_fields = (
        BooleanField('AssignIpv6AddressOnCreation'),
        DictField('Ipv6CidrBlockAssociationSet'),
        TagField('Tags')
    )

    detail_fields = (
        Field('SubnetArn'),
        Field('OutpostArn'),
        Field('OwnerId'),
        Field('AvailabilityZone'),
        Field('AvailabilityZoneId'),
        Field('EnableLniAtDeviceIndex'),
        BooleanField('EnableDns64'),
        BooleanField('Ipv6Native'),
        Field('CustomerOwnedIpv4Pool'),
        BooleanField('MapCustomerOwnedIpOnLaunch'),
        DictField('PrivateDnsNameOptionsOnLaunch'),
    )


@group.app
class Ec2Instance(BaseCliApp):
    name: str = 'instance'
    description: str = 'EC2 instance'

    service_cls: Type[BaseAwsService] = AwsEc2InstanceService

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
        BooleanField('EbsOptimized'),
        BooleanField('EnaSupport'),
        DictField('Placement'),
        DictField('BlockDeviceMappings'),
        DictField('MaintenanceOptions'),
        DictField('Monitoring'),
        DictField('IamInstanceProfile'),
        DictField('NetworkInterfaces'),
        Field('RootDeviceName'),
        Field('RootDeviceType'),
        DictField('SecurityGroups'),
        BooleanField('SourceDestCheck'),
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


@group.app
class Ec2Ami(BaseCliApp):
    name: str = 'ami'
    description: str = 'EC2 AMI'

    service_cls: Type[BaseAwsService] = AwsEc2AmiService

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
        DictField('BlockDeviceMappings'),
        Field('ImageOwnerAlias'),
    )
