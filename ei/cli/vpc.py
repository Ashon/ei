from typer import Typer
from rich.console import Console

from ei.aws import vpc
from ei.core.table import list_table
from ei.core.table import detail_table


console = Console()
app = Typer(name='vpc')


VPC_FIELDS = ['id', 'name', 'etc']


@app.command()
def list():
    results = vpc.list()
    table = list_table(VPC_FIELDS, results)

    console.print(table)


@app.command()
def show(id: int):
    result = vpc.show(id)
    table = detail_table(result)

    console.print(table)
