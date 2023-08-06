import math

from typing import Iterable

from .lp_space import l2


__all__ = [
    "jaccard_sim",
    "cos_sim",
    "angular_dist",
    "angular_sim",
]


def _dot(a: Iterable, b: Iterable):
    return sum(x * y for x, y in zip(a, b))


def jaccard_sim(a: set, b: Iterable) -> float:
    intersection = a.intersection(b)
    union = a.union(b)
    return len(intersection) / len(union)


def cos_sim(a: Iterable, b: Iterable):
    return _dot(a, b) / (l2(a) * l2(b))


def angular_dist(a: Iterable[float], b: Iterable[float]) -> float:
    cos: float = cos_sim(a, b)
    return math.acos(cos) / math.pi


def angular_sim(a: Iterable[float], b: Iterable[float]) -> float:
    return 1 - angular_dist(a, b)
