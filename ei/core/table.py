from typing import Dict
from typing import List

from rich import box
from rich.table import Table


DETAIL_FIELDS = ['key', 'value']


def list_table(fields: List[str], items: List) -> Table:
    table = Table(*fields, box=box.ROUNDED)

    for item in items:
        table.add_row(*[v for v in item])

    return table


def detail_table(item: Dict) -> Table:
    table = Table(*DETAIL_FIELDS, box=box.ROUNDED)

    for key, value in item.items():
        table.add_row(key, value)

    return table
