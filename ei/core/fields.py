from typing import Any
from typing import Callable
from typing import Optional
from typing import Collection

from rich.pretty import pretty_repr


def _serialize(record: Any, raw_value: Any) -> Any:
    return str(raw_value)


def extract_from_tag(key: str):
    def _serialize(record: Any, raw_value: Any):
        if record.get('Tags'):
            found_tag = [
                tag['Value'] for tag in record['Tags']
                if tag['Key'] == key
            ]

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
        return '\n'.join([
            f'[bright_black]{key}[/bright_black]:'
            f' {pretty_repr(value) if isinstance(value, Collection) else value}'
            for key, value in obj.items()
        ])

    def serialize(self, record: Any, raw_value: Any) -> str:
        if type(raw_value) is list:
            return '\n'.join([
                self._render_obj(obj)
                for obj in raw_value
            ])
        else:
            return self._render_obj(raw_value)
