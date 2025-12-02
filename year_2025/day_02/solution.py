from re import findall
from typing import Any


def format_input(sample: bool = False):
    with open("sample_input.txt" if sample else "input.txt") as file:
        return (
            range(int(start), int(end) + 1)  # pyright: ignore[reportAny]
            for start, end in findall(r"(\d+)-(\d+)", file.read())  # pyright: ignore[reportAny]
        )


def part_1():
    return sum(
        [
            n
            for r in format_input()
            for n in r
            if not len(str(n)) % 2
            and str(n)[: len(str(n)) // 2] == str(n)[len(str(n)) // 2 :]
        ]
    )


def part_2():
    return sum(n for r in format_input() for n in r if part_2_helper(n))


def part_2_helper(n: int):
    return any(
        all_same(list(chunkify(str(n), d)))
        for d in range(2, len(str(n)) + 1)
        if not len(str(n)) % d
    )


def chunkify(string: str, parts: int):
    return zip(*[iter(string)] * (len(string) // parts))


def all_same(l: list[Any]):  # pyright: ignore[reportExplicitAny]
    head = l[0]  # pyright: ignore[reportAny]
    return all(i == head for i in l)  # pyright: ignore[reportAny]
