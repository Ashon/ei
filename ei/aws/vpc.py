from typing import Any

from mypy_boto3_ec2 import EC2Client

from ei.core.service import BaseAwsService


class AwsVpcService(BaseAwsService):
    service_name = 'ec2'

    @classmethod
    def _list(cls, client: EC2Client) -> Any:
        return client.describe_vpcs()['Vpcs']

    @classmethod
    def _show(cls, client: EC2Client, id: str) -> Any:
        return client.describe_vpcs(VpcIds=[id])['Vpcs']
