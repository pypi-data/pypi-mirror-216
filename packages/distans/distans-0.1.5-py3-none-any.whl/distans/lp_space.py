from typing import Any, Iterable, Optional

from .utils import T


__all__ = [
    "l1",
    "l2",
    "l_inf",
    "lp",
]


def l1(a: Iterable[T], b: Optional[Iterable[T]] = None) -> T:
    v = _vec(a, b)
    return sum(abs(x) for x in v)  # type: ignore


def l2(a: Iterable[T], b: Optional[Iterable[T]] = None) -> T:
    v = _vec(a, b)
    return sum(x**2 for x in v) ** 0.5


def l_inf(a: Iterable[T], b: Optional[Iterable[T]] = None) -> T:
    v = _vec(a, b)
    return max(abs(x) for x in v)


def lp(a: Iterable[T], b: Optional[Iterable[T]] = None, *, p: Any) -> T:
    inv_p = p**-1
    v = _vec(a, b)
    return sum(abs(x) ** p for x in v) ** inv_p


def _vec(a: Iterable[T], b: Optional[Iterable[T]]) -> Iterable[T]:
    return a if b is None else (x - y for x, y in zip(a, b))
