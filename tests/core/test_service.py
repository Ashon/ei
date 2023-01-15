from contextlib import contextmanager
from contextlib import _GeneratorContextManager
from typing import Any
from typing import Callable
from typing import Generator
from unittest import mock

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


@mock.patch('ei.core.defaults.AWS_REGION', 'region-1')
@mock.patch('ei.core.defaults.EI_REGIONS', ['region-1', 'region-2'])
@mock.patch('ei.core.defaults.EI_ACCOUNT_IDS', ['account-a', 'account-b'])
def test_dummy_service() -> None:
    service = DummyAwsService()

    assert service.service_name == 'dummy'
    items = service.list(region='test-region', account_id='test-account')
    assert items[0]['Region'] == 'test-region'
    assert items[0]['Account'] == 'test-account'

    item = service.show(
        id='1', region='test-region', account_id='test-account')
    assert item['Region'] == 'test-region'
    assert item['Account'] == 'test-account'

    item = service.show(
        id='1', region='', account_id='test-account')
    assert item['Region'] == 'region-1'
    assert item['Account'] == 'test-account'

    item = service.show(
        id='1', region='', account_id='')
    assert item['Region'] == 'region-1'
    assert item['Account'] == 'account-a'
