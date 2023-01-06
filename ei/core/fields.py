from typing import Any
from typing import Callable
from typing import Optional


def _serialize(record: Any, raw_value: Any) -> Any:
    return str(raw_value)


class Field(object):
    _name: str
    serialize: Callable[[Any, Any], str]

    def __init__(self, name: str,
                 serializer: Optional[Callable] = None) -> None:
        self._name = name
        if serializer:
            self.serialize = serializer
        else:
            self.serialize = _serialize

    def __call__(self, record: Any) -> str:
        raw_value = record.get(self._name, '')

        return self.serialize(record, raw_value)


class TagField(Field):
    def serialize(self, record: Any, raw_value: Any) -> str:
        if not raw_value:
            return ''

        return '\n'.join([
            f'{tag["Key"]} = {tag["Value"]}'
            for tag in raw_value
        ])


class DictField(Field):
    def serialize(self, record: Any, raw_value: Any) -> str:
        return '\n'.join([
            '\n'.join([
                f'{key} = {value}'
                for key, value in obj.items()
            ])
            for obj in raw_value
        ])
