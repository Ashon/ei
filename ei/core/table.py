from typing import Dict
from typing import List

from rich import box
from rich.table import Table

from ei.core.fields import Field
from ei.core.fields import IDField


DETAIL_FIELDS = ['key', 'value']


def list_table(fields: List[Field], items: List) -> Table:
    table = Table(box=box.ROUNDED, expand=True)
    for field in fields:
        is_idfield = isinstance(field, IDField)
        table.add_column(
            field._name, no_wrap=is_idfield,
            overflow='fold' if is_idfield else 'ellipsis')

    for item in items:
        table.add_row(*[v for v in item])

    return table


def detail_table(item: Dict) -> Table:
    table = Table(*DETAIL_FIELDS, box=box.ROUNDED)

    for key, value in item.items():
        table.add_row(key, value)

    return table
