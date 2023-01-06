from mypy_boto3_ec2 import EC2Client

from ei.aws import defaults
from ei.aws.session import client_session


def list(region: str):
    if not region:
        region = defaults.AWS_REGION

    result = None

    with client_session(region=region, service_name='ec2') as client:
        client: EC2Client

        result = client.describe_vpcs()
        result = result['Vpcs']

    return result


def show(id: str, region: str):
    if not region:
        region = defaults.AWS_REGION

    result = None

    with client_session(region=region, service_name='ec2') as client:
        client: EC2Client

        result = client.describe_vpcs(VpcIds=[id])
        result = result['Vpcs'][0]

    return result
