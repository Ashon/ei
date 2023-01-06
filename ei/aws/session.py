from typing import Generator
import boto3
from contextlib import contextmanager
from botocore.credentials import DeferredRefreshableCredentials
from botocore.session import Session
from botocore.session import get_session


def create_session(
        account_id: str,
        region_name: str,
        service_name: str) -> boto3.Session.client:
    """Creates client session via sts client
    """

    def _get_session_creds():
        sts_client = boto3.Session().client('sts')

        assumed_role_object: dict = sts_client.assume_role(
            RoleArn=f'arn:aws:iam::{account_id}:role/krp',
            RoleSessionName='AssumeRoleKRP'
        )

        credentials: dict = assumed_role_object['Credentials']
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
    session.set_config_variable('region', region_name)
    session._credentials = credentials

    session = Session(botocore_session=session)

    return session.client(service_name)


@contextmanager
def session(
        account_id: str, region: str,
        service_name: str) -> Generator[Session, None]:

    session = create_session(
        account_id=account_id, region_name=region,
        service_name=service_name)

    yield session
