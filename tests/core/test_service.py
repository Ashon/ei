from unittest import mock

from tests.core.mockup import DummyAwsService


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
