import datetime
from contextlib import contextmanager
from typing import TYPE_CHECKING
from typing import Callable
from typing import Dict
from typing import Generator
from typing import Optional

import boto3
from botocore.credentials import DeferredRefreshableCredentials
from botocore.session import get_session

from ei.core import defaults


if TYPE_CHECKING:
    from botocore.session import Session  # noqa: F401


def from_sts(account_id: str) -> Dict:
    sts_client = boto3.Session().client('sts')

    role_arn = defaults.EI_STS_ASSUME_ROLE_ARN_PATTERN.format(
        account_id=account_id)

    assumed_role_object: dict = sts_client.assume_role(
        RoleArn=role_arn,
        RoleSessionName=defaults.EI_STS_ASSUME_ROLE_SESSION_NAME)

    credentials: dict = assumed_role_object['Credentials']

    return credentials


def from_env(*args: tuple, **kwargs: dict) -> Dict:
    credentials = {
        'AccessKeyId': defaults.AWS_ACCESS_KEY_ID,
        'SecretAccessKey': defaults.AWS_SECRET_ACCESS_KEY,
        'SessionToken': defaults.AWS_SECURITY_TOKEN,
        'Expiration': datetime.datetime.fromisoformat(
            defaults.AWS_SESSION_EXPIRATION)
    }

    return credentials


credential_resolvers = {
    'env': from_env,
    'sts': from_sts
}  # type: Dict[str, Callable]


def create_session(
        service_name: str, account_id: str,
        region: Optional[str] = defaults.AWS_REGION) -> boto3.Session.client:
    """Creates client session via sts client
    """

    credential_resolver: Callable = credential_resolvers[
        defaults.EI_CREDENTIAL_RESOLVER]

    def _get_session_creds() -> Dict:
        credentials = credential_resolver(account_id)

        credential_metadata = {
            'access_key': credentials['AccessKeyId'],
            'secret_key': credentials['SecretAccessKey'],
            'token': credentials['SessionToken'],
            'expiry_time': credentials['Expiration'].isoformat(),
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
        service_name: str, account_id: str,
        region: Optional[str] = defaults.AWS_REGION) -> Generator:
    session = create_session(
        service_name=service_name, account_id=account_id, region=region)

    yield session
