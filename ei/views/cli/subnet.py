from ei.core.cli import BaseCliApp
from ei.core.fields import Field
from ei.core.fields import IDField
from ei.core.fields import TagField
from ei.core.fields import DictField
from ei.core.fields import extract_from_tag
from ei.services.aws.subnet import AwsSubnetService


class SubnetCliApp(BaseCliApp):
    name: str = 'subnet'
    description: str = 'EC2 Subnet'
    service_cls = AwsSubnetService

    short_fields = (
        Field('Region'),
        Field('Account'),
        IDField('SubnetId'),
        Field('Name', serializer=extract_from_tag('Name')),
        Field('CidrBlock'),
        Field('AvailableIpAddressCount'),
        Field('DefaultForAz'),
        Field('MapPublicIpOnLaunch'),
        Field('State'),
        Field('VpcId'),
    )

    long_fields = (
        Field('AssignIpv6AddressOnCreation'),
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
        Field('EnableDns64'),
        Field('Ipv6Native'),
        Field('CustomerOwnedIpv4Pool'),
        Field('MapCustomerOwnedIpOnLaunch'),
        DictField('PrivateDnsNameOptionsOnLaunch'),
    )
