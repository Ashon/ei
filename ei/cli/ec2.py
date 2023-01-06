from ei.cli._base import BaseCliApp
from ei.aws.ec2 import AwsEc2Service
from ei.core.field_serializers import to_string
from ei.core.field_serializers import serialize_tags
# from ei.core.field_serializers import serialize_dict_list


class Ec2CliApp(BaseCliApp):
    name: str = 'ec2'
    description: str = 'EC2 instance'

    service_cls = AwsEc2Service

    short_fields = (
        ('Region', to_string),
        ('Account', to_string),
        ('InstanceId', to_string),
        ('Name', lambda record, value: [
            t['Value'] for t in record['Tags']
            if t['Key'] == 'Name'][0]),
        ('ImageId', to_string),
        ('InstanceType', to_string),
        ('PrivateIpAddress', to_string),
        ('State', lambda record, value: value['Name']),
        ('VpcId', to_string),
    )

    long_fields = (
        ('Placement', to_string),
        ('SubnetId', to_string),
        ('Hypervisor', to_string),
        ('Architecture', to_string),
        # ('MaintenanceOptions', to_string)
        # ('BlockDeviceMappings', to_string),
        # ('CidrBlockAssociationSet', serialize_dict_list),
        ('Tags', serialize_tags)
    )

    detail_fields = (
        ('AmiLaunchIndex', to_string),
        ('LaunchTime', to_string),
        ('Monitoring', to_string),
        ('PrivateDnsName', to_string),
        ('ProductCodes', to_string),
        ('PublicDnsName', to_string),
        ('StateTransitionReason', to_string),
        ('ClientToken', to_string),
        ('EbsOptimized', to_string),
        ('EnaSupport', to_string),
        ('IamInstanceProfile', to_string),
        ('NetworkInterfaces', to_string),
        ('RootDeviceName', to_string),
        ('RootDeviceType', to_string),
        ('SecurityGroups', to_string),
        ('SourceDestCheck', to_string),
        ('VirtualizationType', to_string),
        ('CpuOptions', to_string),
        ('CapacityReservationSpecification', to_string),
        ('HibernationOptions', to_string),
        ('MetadataOptions', to_string),
        ('EnclaveOptions', to_string),
        ('PlatformDetails', to_string),
        ('UsageOperation', to_string),
        ('UsageOperationUpdateTime', to_string),
        ('PrivateDnsNameOptions', to_string),
    )
