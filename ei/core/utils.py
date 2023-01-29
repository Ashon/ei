def to_pascal_case(snake_cased_string: str) -> str:
    parsed = snake_cased_string.split('_')
    parsed = [
        p[0].upper() + p[1:] for p in parsed
    ]

    return ''.join(parsed)
