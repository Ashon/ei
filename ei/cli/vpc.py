from typer import Typer
from rich.console import Console
from botocore.exceptions import ClientError

from ei.aws import vpc
from ei.core.table import list_table
from ei.core.table import detail_table
from ei.core.field_serializers import serialize_tags
from ei.core.field_serializers import serialize_dict_list
from ei.core.data_serializers import serialize_data_as_list
from ei.core.data_serializers import serialize_data_as_dict


console = Console()
app = Typer(name='vpc')


VPC_FIELDS = (
    ('VpcId', str),
    ('OwnerId', str),
    ('InstanceTenancy', str),
    ('IsDefault', str),
    ('State', str),
    ('DhcpOptionsId', str),
    ('CidrBlock', str)
)

MORE_FIELDS = (
    ('CidrBlockAssociationSet', serialize_dict_list),
    ('Tags', serialize_tags)
)

FULL_FIELDS = VPC_FIELDS + MORE_FIELDS


@app.command()
def list(long: bool = False, region: str = ''):
    headers = VPC_FIELDS
    if long:
        headers = FULL_FIELDS

    results = vpc.list(region=region)
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
