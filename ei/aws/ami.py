from itertools import chain

from mypy_boto3_ec2 import EC2Client

from ei.aws import defaults
from ei.aws.base import BaseAwsService


class AwsAmiService(BaseAwsService):
    service_name = 'ec2'

    @classmethod
    def _list(cls, client: EC2Client) -> list[dict]:
        images = client.describe_images(Owners=defaults.EI_ACCOUNT_IDS)['Images']
        return images

    @classmethod
    def _show(cls, client: EC2Client, id: str) -> dict:
        image = client.describe_images(ImageIds=[id])['Images']
        return image
