from functools import cache


def format_input(sample: bool = False):
    with open("sample_input.txt" if sample else "input.txt") as file:
        lines = file.read().strip().split("\n")[::2]
    return lines[0].find("S"), [
        [index for index, value in enumerate(line) if value == "^"] for line in lines
    ][1:]


def split_beam(beams: set[int], splitter: int):
    if splitter in beams:
        beams -= {splitter}
        beams |= {splitter - 1, splitter + 1}
        return 1
    return 0


def part_1():
    beam, splitters = format_input()
    beams = {beam}
    return sum([split_beam(beams, splitter) for row in splitters for splitter in row])


def part_2():
    beam, splitters = format_input()
    splitters = tuple(map(tuple, splitters))
    return part_2_prime(beam, splitters)


@cache
def part_2_prime(beam: int, splitters: tuple[tuple[int]]) -> int:
    return (
        1
        if not splitters
        else part_2_prime(beam - 1, splitters[1:])
        + part_2_prime(beam + 1, splitters[1:])
        if beam in splitters[0]
        else part_2_prime(beam, splitters[1:])
    )


print(part_1())
print(part_2())
