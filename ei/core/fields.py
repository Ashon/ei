import typing
from typing import Any
from typing import Callable
from typing import Optional
from typing import Collection

from rich.pretty import pretty_repr

if typing.TYPE_CHECKING:
    from typing import List  # noqa: F401


def _serialize(record: Any, raw_value: Any) -> Any:
    return str(raw_value)


def extract(key: str) -> Callable:
    def _serialize(record: Any, raw_value: Any) -> str:
        value = raw_value.get(key, '')
        return str(value)

    return _serialize


def extract_from_tag(key: str) -> Callable:
    def _serialize(record: Any, raw_value: Any) -> str:
        if record.get('Tags'):
            found_tag = [
                tag['Value'] for tag in record['Tags']
                if tag['Key'] == key
            ]  # type: List[str]

            if found_tag:
                return found_tag[0]

        return ''

    return _serialize


class Field(object):
    _name: str
    serialize: Callable[[Any, Any], str]

    def __init__(self, name: str,
                 serializer: Optional[Callable] = None) -> None:
        self._name = name
        if serializer:
            self.serialize = serializer
        else:
            if not hasattr(self, 'serialize'):
                self.serialize = _serialize

    def __repr__(self) -> str:
        return (
            f'<{self.__class__.__name__}@{self.__hash__()}: "{self._name}" >'
        )

    def __call__(self, record: Any) -> str:
        raw_value = record.get(self._name, '')

        return self.serialize(record, raw_value)


class IDField(Field):
    def serialize(self, record: Any, raw_value: Any) -> str:
        return f'[bold]{raw_value}[/bold]'


class BooleanField(Field):
    def serialize(self, record: Any, raw_value: Any) -> str:
        color = 'green' if raw_value is True else 'bright_red'
        return f'[{color}]{raw_value}[/{color}]'


class TagField(Field):
    def serialize(self, record: Any, raw_value: Any) -> str:
        if not raw_value:
            return ''

        return '\n'.join([
            f'[bright_black]{tag["Key"]}[/bright_black]: {tag["Value"]}'
            for tag in raw_value
        ])


class DictField(Field):
    def _render_obj(self, obj: dict) -> str:
        if not obj:
            return '[bright_black]None[/bright_black]'

        return '\n'.join([
            f'[bright_black]{key}[/bright_black]: '
            f'{pretty_repr(value) if isinstance(value, Collection) else value}'
            for key, value in obj.items() if key != 'ResponseMetadata'
        ])

    def serialize(self, record: Any, raw_value: Any) -> str:
        if type(raw_value) is list:
            return '\n'.join([
                '\n'.join([
                    (('- ' if idx == 0 else '  ') + line)
                    for idx, line in enumerate(
                        self._render_obj(obj).split('\n'))
                ])
                for obj in raw_value
            ])
        else:
            return self._render_obj(raw_value)
