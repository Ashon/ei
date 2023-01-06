from typer import Typer

from rich.console import Console
from botocore.exceptions import ClientError

from ei.aws import vpc
from ei.aws import defaults
from ei.core.concurrency import bulk_action
from ei.core.table import list_table
from ei.core.table import detail_table
from ei.core.field_serializers import serialize_tags
from ei.core.field_serializers import serialize_dict_list
from ei.core.data_serializers import serialize_data_as_list
from ei.core.data_serializers import serialize_data_as_dict


console = Console()
app = Typer(name='vpc')


VPC_FIELDS = (
    ('Region', str),
    ('VpcId', str),
    ('OwnerId', str),
    ('InstanceTenancy', str),
    ('IsDefault', str),
    ('State', str),
    ('DhcpOptionsId', str),
    ('CidrBlock', str)
)

LONG_FIELDS = (
    ('CidrBlockAssociationSet', serialize_dict_list),
    ('Tags', serialize_tags)
)

FULL_FIELDS = VPC_FIELDS + LONG_FIELDS


@app.command()
def list(
        long: bool = False,
        region: str = '',
        account_id: str = '',
        all_regions: bool = False,
        all_accounts: bool = False):

    if long:
        headers = FULL_FIELDS
    else:
        headers = VPC_FIELDS

    if all_regions:
        regions = defaults.EI_REGIONS
    else:
        regions = [region]

    if all_accounts:
        account_ids = defaults.EI_ACCOUNT_IDS
    else:
        account_ids = [account_id]

    results = bulk_action(vpc.list, regions, account_ids)
    serialized_results = serialize_data_as_list(headers, results)

    table = list_table([h[0] for h in headers], serialized_results)
    console.print(table)


@app.command()
def show(id: str, region: str = ''):
    try:
        result = vpc.show(id, region)
        serialized_result = serialize_data_as_dict(FULL_FIELDS, result)

        table = detail_table(serialized_result)
        console.print(table)

    except ClientError as e:
        print(e)
