from typing import TypeVar, Callable, Any

T = TypeVar('T')

R = TypeVar('R')


def is_last_index(list: list[Any], index: int) -> bool:
    return index == len(list) - 1


def list_range(list: list[T], limit: int = 0, start_index: int = 0) -> list[T]:
    end_index = start_index+limit
    return list[start_index:end_index] if end_index else list


# def map_to(items: list[T], handle_function: Callable[[T, int], R]) -> list[R]:
#     return list(map(handle_function, items, range(len(items))))

def map_to(items: list[T], handle_function: Callable[[T, int], R]) -> list[R]:
    return list(map(handle_function, items, range(len(items))))

# def map_to(items: List[Match[str]], transformer: Callable[[Match[str], int], str]) -> List[str]:
#     return [transformer(item, i) for i, item in enumerate(items)]


def filter_to(items: list[T], handle_function: Callable[[T, int], bool]) -> list[T]:
    result: list[T] = []
    for index, item in enumerate(items):
        if handle_function(item, index):
            result.append(item)
    return result

# def filter(items: list[T], handle_function: Callable[[T], bool]) -> list[T]:
#     return list(filter(handle_function, items))


def get_diff(list1: list[T], list2: list[T]) -> list[T]:
    """Get the difference between two lists.
    Args:
        list1 (list): The first list.
        list2 (list): The second list.
    Returns:
        list: item in list1 not in list2
    """
    return filter_to(list1, lambda item, _: item not in list2)


def get(index: int, default_value: Any = None) -> Callable[[list[Any]], Any | None]:
    """
    Safely gets an element from a list.
    Args:
        list1: The list to be accessed.
        index: The index of the element to be retrieved.
    Returns:
        The element at index `index` in list1, or `None` if the index is out of bounds.
    """
    return lambda items: items[index] if index > -1 and index < len(items) else default_value

# def get(list1:list[Any], index:int):
#   """
#   Safely gets an element from a list.

#   Args:
#     list1: The list to be accessed.
#     index: The index of the element to be retrieved.

#   Returns:
#     The element at index `index` in list1, or `None` if the index is out of bounds.
#   """
#   if index < 0 or index >= len(list1):
#     return None
#   else:
#     return list1[index]

# numbers: list[int] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# def is_even(number: int) -> bool:
#     return number % 2 == 0
# even_numbers = filter(is_even, numbers)

# class ZuiList:
#     def __init__(self, items: list[T]) -> None:
#         self.list: list[T] = items

#     def map(self, handle_function: Callable[[T], R]) -> list[R]:
#         return list(map(handle_function, self.list))

#     def filter(self, items: list[T], handle_function: Callable[[T], bool]) -> list[T]:
#         return list(filter(handle_function, items))


# ZuiList([1, 2, 3]).map(lambda x: x+1)
