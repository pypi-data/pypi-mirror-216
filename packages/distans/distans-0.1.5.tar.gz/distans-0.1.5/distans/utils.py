from typing import Any, Iterable, TypeVar


T = TypeVar("T", bound=Any)


def dot(a: Iterable[T], b: Iterable[T]) -> T:
    return sum(x * y for x, y in zip(a, b))  # type: ignore
