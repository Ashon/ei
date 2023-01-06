from ei.core.cli import BaseCliApp
from ei.core.fields import Field
from ei.core.fields import TagField
from ei.core.fields import DictField
from ei.aws.vpc import AwsVpcService


class VpcCliApp(BaseCliApp):
    name: str = 'vpc'
    description: str = 'EC2 VPC'

    service_cls = AwsVpcService

    short_fields = (
        Field('Region'),
        Field('Account'),
        Field('VpcId'),
        Field('Name', serializer=lambda record, raw_value: [
            tag['Value'] for tag in record['Tags']
            if tag['Key'] == 'Name'
        ][0]),
        Field('InstanceTenancy'),
        Field('IsDefault'),
        Field('State'),
        Field('DhcpOptionsId'),
        Field('CidrBlock')
    )

    long_fields = (
        DictField('CidrBlockAssociationSet'),
        TagField('Tags')
    )
