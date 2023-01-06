from ei.core.cli import BaseCliApp
from ei.core.fields import Field
from ei.core.fields import TagField
from ei.aws.ec2 import AwsEc2Service


class Ec2CliApp(BaseCliApp):
    name: str = 'ec2'
    description: str = 'EC2 instance'

    service_cls = AwsEc2Service

    short_fields = (
        Field('Region'),
        Field('Account'),
        Field('InstanceId'),
        Field('Name', serializer=lambda record, raw_value: [
            tag['Value'] for tag in record['Tags']
            if tag['Key'] == 'Name'
        ][0]),
        Field('ImageId'),
        Field('InstanceType'),
        Field('PrivateIpAddress'),
        Field('State', serializer=lambda record, raw_value: raw_value['Name']),
        Field('VpcId'),
    )

    long_fields = (
        Field('Placement'),
        Field('SubnetId'),
        Field('Hypervisor'),
        Field('Architecture'),
        Field('MaintenanceOptions'),
        Field('BlockDeviceMappings'),
        TagField('Tags')
    )

    detail_fields = (
        Field('AmiLaunchIndex'),
        Field('LaunchTime'),
        Field('Monitoring'),
        Field('PrivateDnsName'),
        Field('ProductCodes'),
        Field('PublicDnsName'),
        Field('StateTransitionReason'),
        Field('ClientToken'),
        Field('EbsOptimized'),
        Field('EnaSupport'),
        Field('IamInstanceProfile'),
        Field('NetworkInterfaces'),
        Field('RootDeviceName'),
        Field('RootDeviceType'),
        Field('SecurityGroups'),
        Field('SourceDestCheck'),
        Field('VirtualizationType'),
        Field('CpuOptions'),
        Field('CapacityReservationSpecification'),
        Field('HibernationOptions'),
        Field('MetadataOptions'),
        Field('EnclaveOptions'),
        Field('PlatformDetails'),
        Field('UsageOperation'),
        Field('UsageOperationUpdateTime'),
        Field('PrivateDnsNameOptions'),
    )
