from typing import Any
from unittest import mock

from tests.mocks.app import DummyAwsCli


@mock.patch('ei.core.cli.defaults')
def test_cli_app_should_returns_stats(mock_defaults: Any) -> None:
    mock_defaults.AWS_REGION = 'test-region'
    mock_defaults.AWS_ACCESS_KEY_ID = 'test-access-key'
    mock_defaults.AWS_SECRET_ACCESS_KEY = 'test-secret-access-key'
    mock_defaults.AWS_SECURITY_TOKEN = 'test-security-token'
    mock_defaults.AWS_SESSION_EXPIRATION = 'test-expiration'

    app = DummyAwsCli()
    app.list()
    app.show('')
