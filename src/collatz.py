from typing import Iterator


def collatz_iter(n: int) -> Iterator[int]:
    while True:
        if n == 1:
            return

        elif n % 2 == 0:
            n = n//2
        
        elif n % 2 == 1:
            n = 3*n + 1

        yield n
