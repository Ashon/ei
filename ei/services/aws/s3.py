from typing import Any

from mypy_boto3_s3 import S3Client

from ei.core.service import BaseAwsService


class AwsS3BucketService(BaseAwsService):
    service_name = 's3'

    @classmethod
    def _list(cls, client: S3Client) -> Any:
        return client.list_buckets()['Buckets']

    @classmethod
    def _show(cls, client: S3Client, id: str) -> Any:
        return client.describe_db_instances(
            DBInstanceIdentifier=id)['DBInstances']
