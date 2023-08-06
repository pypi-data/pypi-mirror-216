from typing import Iterable


__all__ = [
    "jaccard_sim",
]


def jaccard_sim(a: set, b: Iterable) -> float:
    intersection = a.intersection(b)
    union = a.union(b)
    return len(intersection) / len(union)
