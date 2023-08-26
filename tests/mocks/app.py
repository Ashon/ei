from contextlib import contextmanager
from contextlib import _GeneratorContextManager
from typing import Any
from typing import Callable
from typing import Generator

from ei.core.cli import BaseCliApp
from ei.core.fields import Field
from ei.core.service import BaseAwsService


@contextmanager
def with_dummy(account_id: str, region: str, service_name: str) -> Generator:
    yield ''


ITEMS = [
    {'name': 'item-a', 'type': 'a'},
    {'name': 'item-b', 'type': 'a'},
    {'name': 'item-c', 'type': 'b'},
]


class DummyAwsService(BaseAwsService):
    service_name: str = 'dummy'
    _sessioncontext: Callable[..., _GeneratorContextManager] = with_dummy

    @classmethod
    def _list(cls, client: Any) -> Any:
        return ITEMS

    @classmethod
    def _show(cls, client: Any, id: str) -> Any:
        found_item = [item for item in ITEMS if item['name'] == id]
        return found_item


class DummyAwsCli(BaseCliApp):
    name = 'dummy'

    service_cls = DummyAwsService
    stats_fields = ['type']
    short_fields = [
        Field('name'),
    ]

    long_fields = []
