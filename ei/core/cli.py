from collections import defaultdict
from functools import wraps
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Type
from typing import Iterable
from typing import Optional

from typer import Exit
from typer import Typer
from rich.console import Console
from botocore.exceptions import ClientError

from ei.__about__ import VERSION
from ei.core import defaults
from ei.core.fields import Field
from ei.core.service import BaseAwsService
from ei.core.concurrency import bulk_action
from ei.core.exceptions import BaseError
from ei.core.exceptions import PreflightError
from ei.core.exceptions import WrongRegionError
from ei.core.exceptions import WrongAccountError
from ei.core.table import list_table
from ei.core.table import detail_table


TOPK = 10


def create_application(apps: List['Typeable']) -> Typer:
    cli = CliGroup(
        name='ei',
        description=(
            'A[bold green](ei)[/bold green]'
            f' - AWS CLI for humans. ({VERSION})\n\n'
        ),
        apps=apps
    )

    typer = cli.typer()

    @typer.command(help='Show Current Configuration')
    def config() -> None:
        console = Console()
        console.print(defaults.print_config())

    return typer


def _get_typer(name: str, help: str) -> Typer:
    app = Typer(
        name=name,
        help=help,
        no_args_is_help=True,
        rich_markup_mode='rich',
    )
    return app


def _preflight() -> None:
    if not all(defaults.CONFIGS):
        raise PreflightError((
            'Environment variables are not fulfilled.'
            ' Check the environment variables.'
        ))


def _serialize_data_as_list(fields: Iterable[Field],
                            results: Iterable) -> list:
    return [
        [
            serializer(item)
            for serializer in fields
        ] for item in results
    ]


def _serialize_data_as_dict(fields: Iterable[Field], result: Dict) -> Dict:
    serialized = {}

    for field in fields:
        serialized[field._name] = field(result)

    return serialized


class Typeable(object):
    name: str
    description: str = ''

    def typer(self) -> Typer:
        raise NotImplementedError()


def guard_common_errors(fn: Callable) -> Callable:
    """Wrap exposing command function with common Exception handlers

    Common Exceptions:

    - PreflightError: failed to check default configuration (env vars)
    - BaseError, ClientError: Expected Exception from AWS or client
    - NotImplementedError: Not Supported command
    """

    @wraps(fn)
    def _wraps(self: 'BaseCliApp', region: str = '', account_id: str = '',
               *args: tuple, **kwargs: Dict) -> Any:
        try:
            _preflight()
            self._validate_region(region)
            self._validate_acocunt_id(account_id)

        except PreflightError as e:
            self._console.print(e, style='red')
            self._console.print(f'\n{defaults.print_config()}')
            raise Exit(code=1)

        try:
            result = fn(
                self, region=region, account_id=account_id, *args, **kwargs)

            return result

        except (BaseError, ClientError) as e:
            print(e)
            raise Exit(code=1)

        except NotImplementedError:
            self._console.print(
                '[yellow]This command is not supported yet. :grin:[/yellow]')
            raise Exit(code=1)

    return _wraps


class BaseCliApp(Typeable):
    service_cls: Type[BaseAwsService]

    # fields for list
    short_fields: tuple

    # additional fields for long list
    long_fields: tuple

    # more additional fields for show resource
    detail_fields: tuple = ()

    stats_fields = ['Region', 'Account']

    _service: BaseAwsService

    def __init__(self) -> None:
        self._service = self.service_cls()
        self._console = Console()

        self._list_detail_fields = self.short_fields + self.long_fields
        self._full_fields = self._list_detail_fields + self.detail_fields

    def _validate_region(self, region: str) -> None:
        if region and region not in defaults.EI_REGIONS:
            raise WrongRegionError(
                f'region "{region}" is not in "EI_REGIONS"'
                f'(EI_REGIONS={defaults.EI_REGIONS})'
            )

    def _validate_acocunt_id(self, account_id: str) -> None:
        if account_id and account_id not in defaults.EI_ACCOUNT_IDS:
            raise WrongAccountError(
                f'account_id "{account_id}" is not in "EI_ACCOUNT_IDS"'
                f'(EI_ACCOUNT_IDS={defaults.EI_ACCOUNT_IDS})'
            )

    def _defaulting_args(
            self,
            long: bool,
            region: str,
            all_regions: bool,
            account_id: str,
            all_accounts: bool) -> tuple:

        if long:
            fields = self._list_detail_fields
        else:
            fields = self.short_fields

        additional_fields = []
        regions = defaults.EI_REGIONS
        if not all_regions:
            regions = [region]
        else:
            additional_fields.append(Field('Region'))

        account_ids = defaults.EI_ACCOUNT_IDS
        if not all_accounts:
            account_ids = [account_id]
        else:
            additional_fields.append(Field('Account'))

        display_fields = additional_fields + [*fields]

        return (regions, account_ids, display_fields)

    @guard_common_errors
    def list(
            self,
            long: bool = False,
            stat: bool = True,
            table: bool = True,
            region: str = '',
            account_id: str = '',
            all_regions: bool = False,
            all_accounts: bool = False) -> int:
        """List resources
        """

        regions, account_ids, display_fields = self._defaulting_args(
            long, region, all_regions, account_id, all_accounts)

        results = [*bulk_action(self._service.list, regions, account_ids)]
        serialized_results = _serialize_data_as_list(
            display_fields, results)

        if table:
            display_table = list_table([
                field._name for field in display_fields
            ], serialized_results)
            self._console.print(display_table)

        if stat:
            stats_dict: Dict = {}
            for subject in self.stats_fields:
                stats_dict[subject] = defaultdict(int)

                for item in results:
                    stats_dict[subject][
                        str(item.get(subject))] += 1

            self._console.print(
                f'{len(serialized_results)} "{self.name}" items.')

            for subject in self.stats_fields:
                results = list(stats_dict[subject].items())
                results.sort(
                    key=lambda x: x[1], reverse=True)  # type: ignore

                stat_header = f'\n* per {subject}'
                if len(results) > TOPK:
                    stat_header += (
                        f' (top:{TOPK} / total categories:{len(results)})')

                self._console.print(stat_header)
                for key, count in results[:TOPK]:
                    self._console.print(f'  - "{key}": {count} items.')

        return 0

    @guard_common_errors
    def show(
            self,
            id: str,
            region: str = '',
            account_id: str = '') -> int:
        """Show resource
        """

        result = self._service.show(id, region, account_id)
        serialized_result = _serialize_data_as_dict(
            self._full_fields, result)

        table = detail_table(serialized_result)
        self._console.print(table)

        return 0

    def typer(self) -> Typer:
        commands = ['list', 'show']  # type: List[str]
        available_commands = ', '.join([
            f'[bright_blue]{cmd}[/bright_blue]'
            for cmd in commands
        ])

        app = _get_typer(
            name=self.name,
            help=(
                f'{self.description} [bright_black]'
                f'(subcommands: {available_commands})'
                '[/bright_black]'
            )
        )

        for cmd in commands:
            fn = getattr(self, cmd)
            service_fn = getattr(self.service_cls, f'_{cmd}')
            # replace help message to implemented function's docstring.
            app.command(help=service_fn.__doc__)(fn)

        return app


class CliGroup(Typeable):
    _apps: List[Typeable]

    def __init__(
            self,
            name: str,
            description: str,
            apps: Optional[List[Typeable]] = None
            ) -> None:

        self.name = name
        self.description = description
        self._apps = []

        if apps:
            for app in apps:
                self.add(app)

    def app(self, cls: Type[Typeable]) -> None:
        instance = cls()
        self.add(instance)

    def add(self, instance: Typeable) -> None:
        self._apps.append(instance)

    def typer(self) -> Typer:
        group_description = ', '.join([
            f'[bright_blue]{app.name}[/bright_blue]'
            for app in self._apps
        ])

        group = _get_typer(
            name=self.name,
            help=(
                f'{self.description} [bright_black]'
                f'(subcommands: {group_description})'
                '[/bright_black]'
            )
        )

        for app in self._apps:
            group.add_typer(app.typer())

        return group
