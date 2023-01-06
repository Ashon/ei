import json
from functools import partial
from typing import Any

# dump json string with indent
indented_json = partial(json.dumps, indent=2)


def to_string(record: dict, field: Any):
    return str(field)


def serialize_tags(record: dict, aws_tags: dict):
    if not aws_tags:
        return ''

    return '\n'.join([
        f'{t["Key"]} = {t["Value"]}'
        for t in aws_tags
    ])


def serialize_dict_list(record: dict, dict_list: dict):
    return '\n'.join([
        '\n'.join([
            f'{key} = {value}'
            for key, value in obj.items()
        ])
        for obj in dict_list
    ])
