from itertools import chain
from mypy_boto3_ec2 import EC2Client

from ei.core.service import BaseAwsService


class AwsEc2Service(BaseAwsService):
    service_name = 'ec2'

    @classmethod
    def _list(cls, client: EC2Client) -> list[dict]:
        reservations = client.describe_instances()['Reservations']
        instances = [
            reservation['Instances']
            for reservation in reservations
        ]

        instances = chain(*instances)

        return instances

    @classmethod
    def _show(cls, client: EC2Client, id: str) -> list[dict]:
        reservations = client.describe_instances(
            InstanceIds=[id]
        )['Reservations']

        instance = [
            reservation['Instances']
            for reservation in reservations
        ][0]

        return instance
