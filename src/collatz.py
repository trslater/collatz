from typing import Iterator


def build_tree(m: int) -> dict[int, int]:
    T = {}

    for u in range(m, 0, -1):
        if u in T:
            continue

        for v in collatz_iter(u):
            T[u] = v

            u = v

    return T


def collatz_iter(n: int) -> Iterator[int]:
    while True:
        if n == 1:
            return

        elif n % 2 == 0:
            n = n//2
        
        elif n % 2 == 1:
            n = 3*n + 1

        yield n
