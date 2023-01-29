from ei.core.utils import to_pascal_case


def test_snake_case_should_be_replaced_to_pascal_case() -> None:
    assert to_pascal_case('snake_case_string') == 'SnakeCaseString'
