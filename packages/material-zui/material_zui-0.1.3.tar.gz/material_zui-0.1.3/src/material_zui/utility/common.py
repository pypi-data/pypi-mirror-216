from typing import Callable, TypeVar
from functools import reduce

from material_zui.list import map_to

T = TypeVar("T")
R = TypeVar("R")


def pipe(
    func: Callable[[T], R], *funcs: Callable[[T], R]
) -> Callable[[T], R]:
    """Composes multiple functions into a single function.
    Args:
        func: The first function to compose.
        funcs: The remaining functions to compose.

    Returns:
        A function that applies all of the composed functions to its input.
    """
    def composed(x: T) -> R:
        return reduce(lambda x, f: f(x), (func, *funcs), x)  # type: ignore
    return composed  # type: ignore


def pipe_list(
    func: Callable[[T], R], *funcs: Callable[[T], R]
) -> Callable[[list[T]], list[R]]:
    def composed(items: list[T]) -> list[R]:
        return map_to(items, lambda item, _: pipe(func, *funcs)(item))
    return composed  # type: ignore
