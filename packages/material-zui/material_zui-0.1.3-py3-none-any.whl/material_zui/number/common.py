from typing import Any


def to_float(input_value: Any) -> bool:
    try:
        return float(input_value)
    except ValueError:
        return False


def is_int(value: Any) -> bool:
    '''
    use `isinstance(value, int)` not work for case value is `False`
    '''
    return type(value) is int


def is_float(value: Any) -> bool: return type(value) is float
