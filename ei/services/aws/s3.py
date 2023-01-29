import json
from typing import Any

from mypy_boto3_s3 import S3Client
from ei.core.exceptions import ResourceNotfoundError
from ei.core.service import BaseAwsService


class BucketNotFoundError(ResourceNotfoundError):
    pass


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

        bucket = found_bucket[0]

        accel_config = client.get_bucket_accelerate_configuration(Bucket=id)
        acl = client.get_bucket_acl(Bucket=id)
        encryption = client.get_bucket_encryption(Bucket=id)
        location = client.get_bucket_location(Bucket=id)
        logging = client.get_bucket_logging(Bucket=id)
        noti = client.get_bucket_notification(Bucket=id)
        noti_config = client.get_bucket_notification_configuration(Bucket=id)
        policy = client.get_bucket_policy(Bucket=id)
        policy_status = client.get_bucket_policy_status(Bucket=id)
        request_payment = client.get_bucket_request_payment(Bucket=id)
        tag = client.get_bucket_tagging(Bucket=id)['TagSet']
        versioning = client.get_bucket_versioning(Bucket=id)

        obj = {
            'Name': bucket['Name'],
            'CreationDate': bucket['CreationDate'],
            'AccelerateConfiguration': accel_config,
            'ACL': acl,
            'Encryption': encryption,
            'Location': location,
            'Logging': logging,
            'Notification': noti,
            'NotificationConfiguration': noti_config,
            'Policy': {'Policy': json.loads(policy['Policy'])},
            'PolicyStatus': policy_status,
            'RequestPayment': request_payment,
            'TagSet': tag,
            'Versioning': versioning,
        }

        # client.get_bucket_analytics_configuration(Bucket=id)
        # client.get_bucket_cors(Bucket=id)
        # client.get_bucket_intelligent_tiering_configuration(Bucket=id)
        # client.get_bucket_inventory_configuration(Bucket=id)
        # client.get_bucket_lifecycle(Bucket=id)
        # client.get_bucket_lifecycle_configuration(Bucket=id)
        # client.get_bucket_metrics_configuration(Bucket=id)
        # client.get_bucket_ownership_controls(Bucket=id)
        # client.get_bucket_replication(Bucket=id)
        # client.get_bucket_website(Bucket=id)

        return [obj]
