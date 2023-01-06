from typing import Any
from typing import Callable


class Field(object):
    _name: str

    def __init__(self, name: str, serializer: Callable = None) -> None:
        self._name = name
        if serializer:
            self.serialize = serializer

    def serialize(self, record: Any, raw_value: Any) -> Any:
        return str(raw_value)

    def __call__(self, record: Any) -> None:
        raw_value = record.get(self._name, '')

        return self.serialize(record, raw_value)


class TagField(Field):
    def serialize(self, record: Any, raw_value: Any) -> Any:
        if not raw_value:
            return ''

        return '\n'.join([
            f'{tag["Key"]} = {tag["Value"]}'
            for tag in raw_value
        ])


class DictField(Field):
    def serialize(self, record: Any, raw_value: Any) -> Any:
        return '\n'.join([
            '\n'.join([
                f'{key} = {value}'
                for key, value in obj.items()
            ])
            for obj in raw_value
        ])
