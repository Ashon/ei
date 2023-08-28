from typing import Any

from mypy_boto3_rds import RDSClient

from ei.core.service import BaseAwsService


class AwsRdsInstanceService(BaseAwsService):
    service_name = 'rds'
    resource_name = 'DBInstances'

    @classmethod
    def _list(cls, client: RDSClient) -> Any:
        return client.describe_db_instances()

    @classmethod
    def _show(cls, client: RDSClient, id: str) -> Any:
        return client.describe_db_instances(
            DBInstanceIdentifier=id)
