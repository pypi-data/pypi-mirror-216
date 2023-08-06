from pyparsing import Any
from json import dump

from .check import file_exists


def write_json(data: dict[Any, Any] | list[Any], json_path: str, indent: int = 2) -> None:
    '''
    Write data to json file
    @data: is json object or array object
    @indent: space tab
    '''
    with open(json_path, "w") as f:
        dump(data, f, indent=indent)


def write_to_last(file_path: str, text: str) -> None:
    """
    Writes the given text to the last line of the file.
    @file_path: The path to the file.
    @text: The text to write.
    """
    if file_exists(file_path):
        with open(file_path, "r+") as f:
            f.seek(0, 2)
            f.write(text)
    else:
        write(file_path, text)


def write(file_path: str, text: str) -> None:
    """
    Writes an override file with the given content.
    @filename: The name of the override file.
    @content: The content to write to the override file.
    """
    with open(file_path, "w") as f:
        f.write(text)
