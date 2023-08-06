from typing import Iterable, Optional


__all__ = [
    "l1",
    "l2",
    "l_inf",
    "lp",
]


def _vec(a: Iterable, b: Optional[Iterable]) -> Iterable:
    return a if b is None else (x - y for x, y in zip(a, b))


def l1(a: Iterable, b: Optional[Iterable] = None):
    v = _vec(a, b)
    return sum(abs(x) for x in v)


def l2(a: Iterable, b: Optional[Iterable] = None):
    v = _vec(a, b)
    return sum(x**2 for x in v) ** 0.5


def l_inf(a: Iterable, b: Optional[Iterable] = None):
    v = _vec(a, b)
    return max(abs(x) for x in v)


def lp(a: Iterable, b: Optional[Iterable] = None, *, p):
    inv_p = p**-1
    v = _vec(a, b)
    return sum(abs(x) ** p for x in v) ** inv_p
