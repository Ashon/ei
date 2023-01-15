from typing import Any

from mypy_boto3_ec2 import EC2Client

from ei.core.service import BaseAwsService


class AwsSubnetService(BaseAwsService):
    service_name = 'ec2'

    @classmethod
    def _list(cls, client: EC2Client) -> Any:
        return client.describe_subnets()['Subnets']

    @classmethod
    def _show(cls, client: EC2Client, id: str) -> Any:
        return client.describe_subnets(SubnetIds=[id])['Subnets']
