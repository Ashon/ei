import json
from functools import partial


# dump json string with indent
indented_json = partial(json.dumps, indent=2)


def serialize_tags(aws_tags):
    return '\n'.join(
        f'{t["Key"]} = {t["Value"]}' for t in aws_tags
    )


def serialize_dict_list(dict_list):
    return '\n'.join(
        '\n'.join([f'{key} = {value}' for key, value in obj.items()])
        for obj in dict_list
    )
