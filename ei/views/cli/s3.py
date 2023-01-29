# from typing import Type

from ei.core.cli import BaseCliApp
from ei.core.cli import CliGroup
from ei.core.fields import Field
from ei.core.fields import IDField
from ei.core.fields import DictField
from ei.core.fields import TagField
from ei.services.aws.s3 import AwsS3BucketService


group = CliGroup(name='s3', description='AWS S3')


@group.app
class S3BucketCli(BaseCliApp):
    name: str = 'bucket'
    description: str = 'S3 Bucket'

    service_cls = AwsS3BucketService

    stats_fields = ['Region', 'Account']

    short_fields = (
        IDField('Name'),
        Field('CreationDate'),
    )

    long_fields = ()
    detail_fields = (
        DictField('AccelerateConfiguration'),
        DictField('ACL'),
        DictField('Encryption'),
        DictField('Location'),
        DictField('Logging'),
        DictField('Notification'),
        DictField('NotificationConfiguration'),
        DictField('Policy'),
        DictField('PolicyStatus'),
        DictField('RequestPayment'),
        TagField('TagSet'),
        DictField('Versioning'),
    )
