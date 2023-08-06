from re import finditer, compile
from typing import Any, Callable

from material_zui.list import map_to, filter_to


# def list_match(value: str, regex: str, group: int = 0) -> list[str]:
#     pattern = compile(regex)
#     items = map_to(list(finditer(pattern, value)),
#                    lambda match, _: match.group(group))
#     return filter_to(items, lambda item, _: len(item) > 0)


def list_match(regex: str, group: int = 0) -> Callable[[str], list[str]]:
    pattern = compile(regex)

    def matcher(value: str) -> list[str]:
        items = map_to(list(finditer(pattern, value)),
                       lambda match, _: match.group(group))
        return filter_to(items, lambda item, _: len(item) > 0)
    return matcher

# def remove_all(text: str, regex_pattern_to_remove: str) -> str:
#     pattern = compile(regex_pattern_to_remove)
#     return pattern.sub('', text)

# def remove_all(regex_pattern_to_remove: str) -> Callable[[str], str]:
#     pattern = compile(regex_pattern_to_remove)
#     def remove_all_impl(text: str) -> str:
#         return pattern.sub('', text)
#     return remove_all_impl


def remove_all(regex_pattern_to_remove: str) -> Callable[[str], str]:
    pattern = compile(regex_pattern_to_remove)
    return lambda text: pattern.sub('', text)


def remove_special_characters(text: str) -> str:
    """
    The function removes all special characters from a given string.

    @param text: The input text string that may contain special characters
    @type text: str
    @return: The function `remove_special_characters` takes a string `text` as input and removes all
    special characters (i.e., non-alphanumeric characters) from it using a regular expression pattern.
    The function returns the modified string with special characters removed.
    """
    return remove_all('[^\\w\\s]')(text)


def remove_bmp_characters(text: str) -> str:
    """Removes all BMP characters from a string.
    Args:
      text: The string to remove BMP characters from.
    Returns:
      The string with all BMP characters removed.
    """
    return remove_all(r'[^\u0000-\uFFFF]')(text)


def trim_space(text: str) -> str:
    """
    The function takes a string as input, removes any leading or trailing spaces, and replaces any
    consecutive spaces within the string with a single space.

    :param text: A string that may contain extra spaces that need to be trimmed down to a single space
    :type text: str
    :return: The function `trim_space` takes a string `text` as input and returns a new string with all
    consecutive spaces replaced by a single space, and leading/trailing spaces removed.
    """
    pattern = compile('  ')
    return pattern.sub(' ', text.strip())


def not_empty(value: Any) -> bool:
    return value != None and len(value) > 0
