from contextlib import contextmanager
from contextlib import _GeneratorContextManager
from typing import Any
from typing import Callable
from typing import Generator

from ei.core.cli import BaseCliApp
from ei.core.service import BaseAwsService


@contextmanager
def with_dummy(account_id: str, region: str, service_name: str) -> Generator:
    yield ''


class DummyAwsService(BaseAwsService):
    service_name: str = 'dummy'
    _sessioncontext: Callable[..., _GeneratorContextManager] = with_dummy

    @classmethod
    def _list(cls, client: Any) -> Any:
        return [{}]

    @classmethod
    def _show(cls, client: Any, id: str) -> Any:
        return [{}]


class DummyAwsCli(BaseCliApp):
    name = 'dummy'

    service_cls = DummyAwsService

    short_fields = ()
    long_fields = ()
