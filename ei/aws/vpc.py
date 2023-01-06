from mypy_boto3_ec2 import EC2Client

from ei.aws import defaults
from ei.aws.session import client_session


def list(region: str, account_id: str):
    if not region:
        region = defaults.AWS_REGION

    if not account_id:
        account_id = defaults.EI_ACCOUNT_IDS[0]

    result = None

    with client_session(
            account_id=account_id, region=region,
            service_name='ec2') as client:
        client: EC2Client

        result = client.describe_vpcs()
        result = [{'Region': region, **obj} for obj in result['Vpcs']]

    return result


def show(id: str, region: str, account_id: str):
    if not region:
        region = defaults.AWS_REGION

    if not account_id:
        account_id = defaults.EI_ACCOUNT_IDS[0]

    result = None

    with client_session(
            account_id=account_id, region=region,
            service_name='ec2') as client:
        client: EC2Client

        result = client.describe_vpcs(VpcIds=[id])
        result = [{'Region': region, **obj} for obj in result['Vpcs']][0]

    return result
