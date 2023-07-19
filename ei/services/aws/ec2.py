from typing import Any
from itertools import chain

from mypy_boto3_ec2 import EC2Client

from ei.core import defaults
from ei.core.service import BaseAwsService


class AwsEc2VpcService(BaseAwsService):
    service_name = 'ec2'

    @classmethod
    def _list(cls, client: EC2Client) -> Any:
        return client.describe_vpcs()['Vpcs']

    @classmethod
    def _show(cls, client: EC2Client, id: str) -> Any:
        return client.describe_vpcs(VpcIds=[id])['Vpcs']


class AwsEc2SubnetService(BaseAwsService):
    service_name = 'ec2'

    @classmethod
    def _list(cls, client: EC2Client) -> Any:
        return client.describe_subnets()['Subnets']

    @classmethod
    def _show(cls, client: EC2Client, id: str) -> Any:
        return client.describe_subnets(SubnetIds=[id])['Subnets']


class AwsEc2InstanceService(BaseAwsService):
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


class AwsEc2AmiService(BaseAwsService):
    service_name = 'ec2'

    @classmethod
    def _list(cls, client: EC2Client) -> Any:
        images = client.describe_images(
            Owners=defaults.EI_ACCOUNT_IDS)['Images']
        return images

    @classmethod
    def _show(cls, client: EC2Client, id: str) -> Any:
        image = client.describe_images(ImageIds=[id])['Images']

        return image


class AwsEc2RouteTableService(BaseAwsService):
    service_name = 'ec2'

    @classmethod
    def _list(cls, client: EC2Client) -> Any:
        route_tables = client.describe_route_tables()['RouteTables']
        return route_tables

    @classmethod
    def _show(cls, client: EC2Client, id: str) -> Any:
        route_table = client.describe_route_tables(
            RouteTableIds=[id])['RouteTables']

        return route_table
