from typer import Typer
from rich.console import Console
from botocore.exceptions import ClientError

from ei.aws import defaults
from ei.aws.base import BaseAwsService
from ei.core.concurrency import bulk_action
from ei.core.table import list_table
from ei.core.table import detail_table
from ei.core.data_serializers import serialize_data_as_list
from ei.core.data_serializers import serialize_data_as_dict


class BaseCliApp(object):
    name: str
    service_cls: BaseAwsService

    short_fields: tuple
    long_fields: tuple
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

        if long:
            headers = self._list_detail_fields
        else:
            headers = self.short_fields

        if all_regions:
            regions = defaults.EI_REGIONS
        else:
            regions = [region]

        if all_accounts:
            account_ids = defaults.EI_ACCOUNT_IDS
        else:
            account_ids = [account_id]

        try:
            results = bulk_action(self._service.list, regions, account_ids)
            serialized_results = serialize_data_as_list(headers, results)

            table = list_table([h[0] for h in headers], serialized_results)
            self._console.print(table)

        except ClientError as e:
            print(e)

    def show(
            self,
            id: str,
            region: str = '',
            account_id: str = '') -> None:

        try:
            result = self._service.show(id, region, account_id)
            serialized_result = serialize_data_as_dict(
                self._full_fields, result)

            table = detail_table(serialized_result)
            self._console.print(table)

        except ClientError as e:
            print(e)

    def typer(self):
        app = Typer(name=self.name)

        app.command()(self.list)
        app.command()(self.show)

        return app
