import pytest
from ei.core.fields import extract
from ei.core.fields import extract_from_tag
from ei.core.fields import Field
from ei.core.fields import DictField
from ei.core.fields import IDField
from ei.core.fields import BooleanField
from ei.core.fields import TagField


@pytest.mark.parametrize(['field', 'obj', 'expected'], argvalues=[
    ('field-a', {'field-a': 'expected'}, 'expected'),
    ('field-a', {'field-b': 'not expected'}, ''),
])
def test_field(field: str, obj: dict, expected: str) -> None:
    serializer = Field(field)
    value = serializer(obj)
    assert value == expected


@pytest.mark.parametrize(['field', 'obj', 'expected'], argvalues=[
    ('true-key', {'true-key': True}, '[green]True[/green]'),
    ('false-key', {'false-key': False}, '[bright_red]False[/bright_red]'),
])
def test_booleanfield(field: str, obj: dict, expected: str) -> None:
    serializer = BooleanField(field)
    true_value = serializer(obj)
    assert true_value == expected


@pytest.mark.parametrize(['field', 'key', 'obj', 'expected'], argvalues=[
    ('dict', 'key', {'dict': {'key': 'expected'}}, 'expected'),
    ('dict', 'no-key', {'dict': {'key': 'expected'}}, ''),
])
def test_field_with_extract(field: str, key: str,
                            obj: dict, expected: str) -> None:
    serializer = Field(field, serializer=extract(key))
    value = serializer(obj)
    assert value == expected


@pytest.mark.parametrize(['field', 'key', 'obj', 'expected'], argvalues=[
    ('tags', 'name', {'Tags': [{'Key': 'name', 'Value': 'john'}]}, 'john'),
    ('tags', 'no-key', {'Tags': [{'Key': 'name', 'Value': 'john'}]}, ''),
    ('tags', 'no-key', {'no-tag': ''}, ''),
])
def test_field_with_extract_from_tag(field: str, key: str,
                                     obj: dict, expected: str) -> None:
    serializer = Field(field, serializer=extract_from_tag(key))
    value = serializer(obj)
    assert value == expected


def test_extract_should_returns_extracted_value_from_dict() -> None:
    serializer = extract('expected-key')
    value = serializer({}, {'expected-key': 'expected-value'})
    assert value == 'expected-value'


def test_idfield_should_returns_formatted_string() -> None:
    field = IDField('id')
    value = field({'id': 1})
    assert value == '[bold]1[/bold]'


def test_tagfield_should_returns_formatted_string() -> None:
    serializer = TagField('Tags')
    value = serializer({
        'Tags': [
            {'Key': 'name', 'Value': 'john'},
            {'Key': 'species', 'Value': 'human'}
        ]
    })

    assert value == (
        '[bright_black]name[/bright_black]: john\n'
        '[bright_black]species[/bright_black]: human'
    )

    value = serializer({'Tags': []})

    assert value == ''


def test_dictfield_should_returns_formatted_string() -> None:
    serializer = DictField('Object')
    value = serializer({
        'Object': {
            'Key': 'Value'
        }
    })

    assert value == "[bright_black]Key[/bright_black]: 'Value'"


def test_dictfield_should_returns_formatted_string_when_empty_value() -> None:
    serializer = DictField('Object')
    value = serializer({
        'Object': None
    })

    assert value == '[bright_black]None[/bright_black]'


def test_dictfield_should_ignores_response_metadata() -> None:
    serializer = DictField('Object')
    value = serializer({
        'Object': {
            'Key': 'Value'
        },
        'ResponseMetadata': {}
    })

    assert value == "[bright_black]Key[/bright_black]: 'Value'"


def test_dictfield_should_returns_if_dictlist() -> None:
    serializer = DictField('Object')
    value = serializer({
        'Object': [{
            'KeyA': 'ValueA'
        }, {
            'KeyB': 'ValueB'
        }],
        'ResponseMetadata': {}
    })

    assert value == '\n'.join([
        "- [bright_black]KeyA[/bright_black]: 'ValueA'",
        "- [bright_black]KeyB[/bright_black]: 'ValueB'"
    ])
