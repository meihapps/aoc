from functools import reduce
from itertools import zip_longest
from operator import add, mul


def format_input(sample: bool = False):
    with open("sample_input.txt" if sample else "input.txt") as file:
        *numbers, operators = file.read().strip().split("\n")
    splits = [index - 1 for index, op in enumerate(operators) if op != " "]
    parts = [
        [number[i + 1 : j] for i, j in zip(splits, splits[1:] + [None])]
        for number in numbers
    ]
    return list(zip(zip(*parts), operators.split()))


def parse_column_part_1(x: tuple[tuple[str, ...], str]):
    return [int(n) for n in x[0]], add if x[1] == "+" else mul


def part_1():
    return sum(
        reduce(op, numbers)
        for numbers, op in list(map(parse_column_part_1, format_input()))
    )


def parse_column_part_2(x: tuple[tuple[str, ...], str]):
    return [
        int("".join(number)) for number in zip_longest(*x[0], fillvalue=" ")
    ], add if x[1] == "+" else mul


def part_2():
    return sum(
        reduce(op, numbers)
        for numbers, op in list(map(parse_column_part_2, format_input()))
    )
