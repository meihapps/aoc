# day 7: laboratories

this is a fun one. basically you're making a line straight down. whenever you run into a splitter, the line splits and continues going straight down 1 space to the left and 1 space to the right of where it split.

## formatting the input

```py
def format_input(sample: bool = False):
    with open("sample_input.txt" if sample else "input.txt") as file:
        lines = file.read().strip().split("\n")[::2]
    return lines[0].find("S"), [
        [index for index, value in enumerate(line) if value == "^"] for line in lines
    ][1:]
```

here we're taking every other line - the rest contribute nothing to solving the problem - and producing a list of all the splitters on each line.
we return that alongside the start point on line 0.

## part 1

in this part, you're finding out how many times a splitter gets hit. bear in mind - if two splitters trigger placing a line into the same spot, both splitters still triggered but only one line continues going down that spot.

so first we need to be able to split a beam:

```py
def split_beam(beams: set[int], splitter: int):
    if splitter in beams:
        beams -= {splitter}
        beams |= {splitter - 1, splitter + 1}
        return 1
    return 0
```

this is quite simple - if the beam is meant to split, split it and return 1, otherwise return 0. then we can just get the sum of running this on each splitter on each row to get the answer.

```py
def part_1():
    beam, splitters = format_input()
    beams = {beam}
    return sum([split_beam(beams, splitter) for row in splitters for splitter in row])
```

## part 2

for this part, instead we want to find out how many unique paths down exist.

at each step we're going to want to cover 3 cases:
- we have reached the end of the path
- we haven't reached the end of the path and are splitting
- we haven't reached the end of the path and are not splitting

if we reach the end of the path, we just want to return a 1 as that was 1 path that we reached the end of.
if we haven't reached the end of the path and are splitting, we're going to want to get the outcome if we split left and add that to the outcome if we split right.
if we haven't reached the end of the path and are not splitting, we can just get the outcome if we go straight down.

```py
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
```

here is that as code, using a functools cache to make it faster (`@cache`). what this does is keep track of what inputs led to what outputs, so that when you use the same inputs a second time (which can happen a lot in this kind of problem), you don't need to compute it this time around.

then the part 2 function is just going to wrap around it:

```py
def part_2():
    beam, splitters = format_input()
    splitters = tuple(map(tuple, splitters))
    return part_2_prime(beam, splitters)
```
