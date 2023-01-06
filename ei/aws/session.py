import datetime
from contextlib import contextmanager
from typing import TYPE_CHECKING
from typing import Generator

import boto3
from botocore.credentials import DeferredRefreshableCredentials
from botocore.session import get_session

from ei.aws import defaults


if TYPE_CHECKING:
    from botocore.session import Session  # noqa: F401


def from_env():
    credentials = {
        'AccessKeyId': defaults.AWS_ACCESS_KEY_ID,
        'SecretAccessKey': defaults.AWS_SECRET_ACCESS_KEY,
        'SessionToken': defaults.AWS_SECURITY_TOKEN,
        'Expiration': datetime.datetime.fromisoformat(
            defaults.AWS_SESSION_EXPIRATION)
    }

    return credentials


def create_session(
        service_name: str,
        region: str = defaults.AWS_REGION) -> boto3.Session.client:
    """Creates client session via sts client
    """

    def _get_session_creds():
        credentials = from_env()

        credential_metadata = {
            'access_key': credentials.get('AccessKeyId'),
            'secret_key': credentials.get('SecretAccessKey'),
            'token': credentials.get('SessionToken'),
            'expiry_time': credentials.get('Expiration').isoformat(),
        }

        return credential_metadata

    credentials = DeferredRefreshableCredentials(
        refresh_using=_get_session_creds, method='sts-assume-role')

    session = get_session()  # type: Session
    session.set_config_variable('region', region)
    session._credentials = credentials

    session = boto3.Session(botocore_session=session)

    return session.client(service_name)


@contextmanager
def client_session(
        service_name: str,
        region: str = defaults.AWS_REGION) -> Generator:
    session = create_session(service_name=service_name, region=region)

    yield session
