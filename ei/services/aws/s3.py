import json
from typing import Any

from mypy_boto3_s3 import S3Client
from ei.core.exceptions import ResourceNotfoundError
from ei.core.service import BaseAwsService
from ei.core.utils import to_pascal_case


class BucketNotFoundError(ResourceNotfoundError):
    pass


S3_PROPERTY_FETCHER = {
    'get': (
        'accelerate_configuration',
        'acl',
        'encryption',
        'location',
        'logging',
        'notification',
        'notification_configuration',
        'policy',
        'policy_status',
        'request_payment',
        'tagging',
        'versioning',
        'cors',
        'lifecycle',
        'lifecycle_configuration',
        'ownership_controls',
        'replication',
        'website',
    ),
    'list': (
        'analytics_configurations',
        'intelligent_tiering_configurations',
        'inventory_configurations',
        'metrics_configurations',
    ),
}


class AwsS3BucketService(BaseAwsService):
    service_name = 's3'

    @classmethod
    def _list(cls, client: S3Client) -> Any:
        return client.list_buckets()['Buckets']

    @classmethod
    def _show(cls, client: S3Client, id: str) -> Any:
        bucket_list = cls._list(client)
        found_bucket = [b for b in bucket_list if b['Name'] == id]
        if not found_bucket:
            raise BucketNotFoundError(id)

        bucket = {**found_bucket[0]}
        for method, properties in S3_PROPERTY_FETCHER.items():
            for property in properties:
                fetcher = getattr(client, f'{method}_bucket_{property}')

                try:
                    result = fetcher(Bucket=id)
                    bucket[to_pascal_case(property)] = {**result}
                except Exception:
                    pass

        bucket['Tagging'] = bucket['Tagging']['TagSet']
        if bucket.get('Policy'):
            bucket['Policy'] = json.loads(bucket['Policy'].get('Policy', '{}'))

        return [bucket]
