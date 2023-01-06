from ei.cli.base import BaseCliApp
from ei.aws.ec2 import AwsEc2Service
from ei.core.field_serializers import serialize_tags
# from ei.core.field_serializers import serialize_dict_list


class Ec2CliApp(BaseCliApp):
    name: str = 'ec2'
    service_cls = AwsEc2Service

    short_fields = (
        ('Region', str),
        ('Account', str),
        ('InstanceId', str),
        # ('AmiLaunchIndex', str),
        ('ImageId', str),
        ('InstanceType', str),
        ('PrivateIpAddress', str),
        # ('LaunchTime', str),
        # ('Monitoring', str),
        # ('PrivateDnsName', str),
        # ('ProductCodes', str),
        # ('PublicDnsName', str),
        ('State', lambda x: x['Name']),
        # ('StateTransitionReason', str),
        ('VpcId', str),
        ('SubnetId', str),
        ('Hypervisor', str),
        ('Architecture', str),
        # ('ClientToken', str),
        # ('EbsOptimized', str),
        # ('EnaSupport', str),
        # ('IamInstanceProfile', str),
        # ('NetworkInterfaces', str),
        # ('RootDeviceName', str),
        # ('RootDeviceType', str),
        # ('SecurityGroups', str),
        # ('SourceDestCheck', str),
        # ('VirtualizationType', str),
        # ('CpuOptions', str),
        # ('CapacityReservationSpecification', str),
        # ('HibernationOptions', str),
        # ('MetadataOptions', str),
        # ('EnclaveOptions', str),
        # ('PlatformDetails', str),
        # ('UsageOperation', str),
        # ('UsageOperationUpdateTime', str),
        # ('PrivateDnsNameOptions', str),
    )

    long_fields = (
        ('Placement', str),
        # ('MaintenanceOptions', str)
        # ('BlockDeviceMappings', str),
        # ('CidrBlockAssociationSet', serialize_dict_list),
        ('Tags', serialize_tags)
    )
