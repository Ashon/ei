from typer import Typer
from rich.console import Console
from botocore.exceptions import ClientError

from ei.aws import _defaults
from ei.aws._base import BaseAwsService
from ei.core.concurrency import bulk_action
from ei.core.table import list_table
from ei.core.table import detail_table


class PreflightError(RuntimeError):
    pass


def _preflight():
    if not all(_defaults.CONFIGS):
        raise PreflightError('\n'.join((
            (
                'Environment variables are not fulfilled.'
                ' Check the environment variables.'
            ),
            '',
            f'{_defaults.EI_ACCOUNT_IDS=}',
            f'{_defaults.EI_REGIONS=}',
            f'{_defaults.EI_ASSUME_ROLE_ARN_PATTERN=}',
            f'{_defaults.EI_ASSUME_ROLE_SESSION_NAME=}',
            f'{_defaults.AWS_REGION=}',
            f'{_defaults.AWS_ACCESS_KEY_ID=}',
            f'{_defaults.AWS_SECRET_ACCESS_KEY=}',
            f'{_defaults.AWS_SECURITY_TOKEN=}',
            f'{_defaults.AWS_SESSION_EXPIRATION=}',
        )))


def _serialize_data_as_list(headers, results):
    return [
        [
            serializer(item, item.get(field, ''))
            for field, serializer in headers
        ] for item in results
    ]


def _serialize_data_as_dict(headers, result):
    serialized = {}

    for field, serializer in headers:
        raw_value = result.get(field, '')
        serialized[field] = serializer(result, raw_value)

    return serialized


class BaseCliApp(object):
    name: str
    description: str = ''

    service_cls: BaseAwsService

    # fields for list
    short_fields: tuple

    # additional fields for long list
    long_fields: tuple

    # more additional fields for show resource
    detail_fields: tuple = ()

    _service: object

    def __init__(self):
        self._service = self.service_cls()  # type: BaseAwsService
        self._console = Console()

        self._list_detail_fields = self.short_fields + self.long_fields
        self._full_fields = self._list_detail_fields + self.detail_fields

    def list(
            self,
            long: bool = False,
            region: str = '',
            account_id: str = '',
            all_regions: bool = False,
            all_accounts: bool = False) -> None:

        _preflight()

        if long:
            headers = self._list_detail_fields
        else:
            headers = self.short_fields

        if all_regions:
            regions = _defaults.EI_REGIONS
        else:
            regions = [region]

        if all_accounts:
            account_ids = _defaults.EI_ACCOUNT_IDS
        else:
            account_ids = [account_id]

        try:
            results = bulk_action(self._service.list, regions, account_ids)
            serialized_results = _serialize_data_as_list(headers, results)

            table = list_table([h[0] for h in headers], serialized_results)
            self._console.print(table)

        except ClientError as e:
            print(e)

    def show(
            self,
            id: str,
            region: str = '',
            account_id: str = '') -> None:

        _preflight()

        try:
            result = self._service.show(id, region, account_id)
            serialized_result = _serialize_data_as_dict(
                self._full_fields, result)

            table = detail_table(serialized_result)
            self._console.print(table)

        except ClientError as e:
            print(e)

    def typer(self):
        app = Typer(name=self.name, help=self.description)

        app.command()(self.list)
        app.command()(self.show)

        return app
