import typing
from typing import List
from typing import Type
from typing import Iterable
from typing import Optional

from typer import Typer
from rich.console import Console
from botocore.exceptions import ClientError

from ei.__about__ import VERSION
from ei.core import defaults
from ei.core.fields import Field
from ei.core.service import BaseAwsService
from ei.core.concurrency import bulk_action
from ei.core.exceptions import PreflightError
from ei.core.exceptions import WrongRegionError
from ei.core.exceptions import WrongAccountError
from ei.core.table import list_table
from ei.core.table import detail_table


if typing.TYPE_CHECKING:
    from typing import Callable  # noqa: F401


def create_application(apps: List['Typeable']) -> Typer:
    cli = CliGroup(
        name='ei',
        description=(
            'A[bold green](ei)[/bold green]'
            f' - AWS CLI for humans. ({VERSION})\n\n'
        ),
        apps=apps
    )

    return cli.typer()


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
        raise PreflightError('\n'.join((
            (
                'Environment variables are not fulfilled.'
                ' Check the environment variables.'
            ),
            '',
            f'{defaults.EI_ACCOUNT_IDS=}',
            f'{defaults.EI_REGIONS=}',
            f'{defaults.EI_ASSUME_ROLE_ARN_PATTERN=}',
            f'{defaults.EI_ASSUME_ROLE_SESSION_NAME=}',
            f'{defaults.AWS_REGION=}',
            f'{defaults.AWS_ACCESS_KEY_ID=}',
            f'{defaults.AWS_SECRET_ACCESS_KEY=}',
            f'{defaults.AWS_SECURITY_TOKEN=}',
            f'{defaults.AWS_SESSION_EXPIRATION=}',
        )))


def _serialize_data_as_list(fields: Iterable[Field],
                            results: Iterable) -> list:
    return [
        [
            serializer(item)
            for serializer in fields
        ] for item in results
    ]


def _serialize_data_as_dict(fields: Iterable[Field], result: dict) -> dict:
    serialized = {}

    for field in fields:
        serialized[field._name] = field(result)

    return serialized


class Typeable(object):
    name: str
    description: str = ''

    def typer(self) -> Typer:
        raise NotImplementedError()


class BaseCliApp(Typeable):
    service_cls: Type[BaseAwsService]

    # fields for list
    short_fields: tuple

    # additional fields for long list
    long_fields: tuple

    # more additional fields for show resource
    detail_fields: tuple = ()

    _service: BaseAwsService

    def __init__(self) -> None:
        self._service = self.service_cls()
        self._console = Console()

        self._list_detail_fields = self.short_fields + self.long_fields
        self._full_fields = self._list_detail_fields + self.detail_fields

    def _validate_region(self, region: str) -> None:
        if region and region not in defaults.EI_REGIONS:
            raise WrongRegionError(
                f'{region=} is not in "EI_REGIONS"'
                f'({defaults.EI_REGIONS=})'
            )

    def _validate_acocunt_id(self, account_id: str) -> None:
        if account_id and account_id not in defaults.EI_ACCOUNT_IDS:
            raise WrongAccountError(
                f'{account_id=} is not in "EI_ACCOUNT_IDS"'
                f'({defaults.EI_ACCOUNT_IDS=})'
            )

    def list(
            self,
            long: bool = False,
            stat: bool = True,
            region: str = '',
            account_id: str = '',
            all_regions: bool = False,
            all_accounts: bool = False) -> int:
        """List resources
        """

        try:
            _preflight()
            self._validate_region(region)
            self._validate_acocunt_id(account_id)

        except PreflightError as e:
            self._console.print(e)
            return 1

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
        try:
            results = bulk_action(self._service.list, regions, account_ids)
            serialized_results = _serialize_data_as_list(
                display_fields, results)

            table = list_table([
                field._name for field in display_fields
            ], serialized_results)
            self._console.print(table)

            if stat:
                self._console.print(
                    f'{len(serialized_results)} "{self.name}" items.')

        except ClientError as e:
            print(e)
            return 1

        return 0

    def show(
            self,
            id: str,
            region: str = '',
            account_id: str = '') -> int:
        """Show resource
        """
        try:
            _preflight()
            self._validate_region(region)

        except PreflightError as e:
            self._console.print(e)
            return 1

        try:
            result = self._service.show(id, region, account_id)
            serialized_result = _serialize_data_as_dict(
                self._full_fields, result)

            table = detail_table(serialized_result)
            self._console.print(table)

        except ClientError as e:
            print(e)
            return 1

        return 0

    def typer(self) -> Typer:
        commands = [
            self.list,
            self.show
        ]  # type: List[Callable]
        available_commands = ', '.join([
            f'[bright_blue]{cmd.__name__}[/bright_blue]'
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
            app.command()(cmd)

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
