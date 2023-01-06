from mypy_boto3_ec2 import EC2Client

from ei.aws._base import BaseAwsService


class AwsVpcService(BaseAwsService):
    service_name = 'ec2'

    @classmethod
    def _list(cls, client: EC2Client) -> list[dict]:
        return client.describe_vpcs()['Vpcs']

    @classmethod
    def _show(cls, client: EC2Client, id: str) -> list[dict]:
        return client.describe_vpcs(VpcIds=[id])['Vpcs']
