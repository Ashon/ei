from ei.core.cli import BaseCliApp
from ei.core.fields import Field
from ei.core.fields import IDField
from ei.core.fields import TagField
from ei.core.fields import DictField
from ei.core.fields import extract_from_tag
from ei.services.aws.vpc import AwsVpcService


class VpcCliApp(BaseCliApp):
    name: str = 'vpc'
    description: str = 'EC2 VPC'

    service_cls = AwsVpcService

    short_fields = (
        Field('Region'),
        Field('Account'),
        IDField('VpcId'),
        Field('Name', serializer=extract_from_tag('Name')),
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
