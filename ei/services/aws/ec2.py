from typing import Any
from itertools import chain

from mypy_boto3_ec2 import EC2Client

from ei.core.service import BaseAwsService


class AwsEc2Service(BaseAwsService):
    service_name = 'ec2'

    @classmethod
    def _list(cls, client: EC2Client) -> Any:
        reservations = client.describe_instances()['Reservations']
        instances = [
            reservation['Instances']
            for reservation in reservations
        ]

        iterable = chain(*instances)

        return iterable

    @classmethod
    def _show(cls, client: EC2Client, id: str) -> Any:
        reservations = client.describe_instances(
            InstanceIds=[id]
        )['Reservations']

        instance = [
            reservation['Instances']
            for reservation in reservations
        ][0]

        return instance
