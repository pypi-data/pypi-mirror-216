from typing import Sequence


__all__ = [
    "jaro_sim",
    "jaro_winkler_sim",
]


def jaro_sim(s1: Sequence, s2: Sequence) -> float:
    if s1 == s2:
        return 1.0

    len_s1 = len(s1)
    len_s2 = len(s2)

    match_bound = max(len_s1, len_s2) // 2 - 1

    matches = 0
    pos1 = []
    pos2 = []

    for i, ch1 in enumerate(s1):
        upper = min(i + match_bound + 1, len_s2)
        lower = max(0, i - match_bound)
        for j in range(lower, upper):
            if ch1 == s2[j] and j not in pos2:
                matches += 1
                pos1.append(i)
                pos2.append(j)
                break

    if matches == 0:
        return 0.0

    pos2.sort()
    transpositions = 0
    for i, j in zip(pos1, pos2):
        if s1[i] != s2[j]:
            transpositions += 1

    a = matches / len_s1
    b = matches / len_s2
    c = (matches - transpositions // 2) / matches
    return (a + b + c) / 3


def jaro_winkler_sim(
    s1: Sequence,
    s2: Sequence,
    p: float = 0.1,
    max_l: int = 4,
) -> float:
    assert 0 <= max_l * p <= 1
    jaro = jaro_sim(s1, s2)

    l = 0
    for ch1, ch2 in zip(s1, s2):
        if ch1 == ch2:
            l += 1
        else:
            break
        if l == max_l:
            break
    return jaro + (l * p * (1 - jaro))
