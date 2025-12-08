# day 6: trash compactor

this problem is primarily about parsing the input. basically somebody is using the world's worst layout for their maths equations and you have to solve the equations.

## part 1

here you have guessed at what the layout means and assumed that each column is a set of numbers with an operation to do between them at the end. i.e.
```
1 5
2 6
3 7
4 8
+ *
```
would be
```
1+2+3+4 = 10
5*6*7*8 = 1680
```

so it isn't all that difficult. you can simply split on new lines to get each row, split those rows on spaces to get each number and then use `zip(*rows_after_splitting_on_space)` to transpose it. this is what i was doing before, but that code is gone now because i wanted format_input to be usable on both parts and that code does not at all work for part 2.

after that, you can simply do one of these to the formatted input:

```py
def parse_column_part_1(x: tuple[tuple[str, ...], str]):
    return [int(n) for n in x[0]], add if x[1] == "+" else mul

def part_1():
    return sum(
        reduce(op, numbers)
        for numbers, op in list(map(parse_column_part_1, format_input()))
    )
```

first we turn each column into a tuple holding a list of integers and the operator between them, then we reduce the list with the operator as the function.

## part 2

this is where you realise how awful this theoretical persons math notes are. the true layout is far, far worse.

```
123 328  51 64
 45 64  387 23
  6 98  215 314
*   +   *   +
```

this example is not `123 * 45 * 6` like you would expect. it's instead `1 * 24 * 356`. you go down the columns.

parsing this is a challenge for one reason. numbers can have white space before OR after them and their position does matter so you can't strip that whitespace away until the very end. this means anything using `.split()` will fail because you can't split on space and still have spaces.

this makes the operators at the bottom the only effective source of truth for when to split - at the index before any given operator.

this makes it mostly fine but if you're really trying to stick with the pythonic approach this will probably be the last thing you want to try.

```py
def format_input(sample: bool = False):
    with open("sample_input.txt" if sample else "input.txt") as file:
        *numbers, operators = file.read().strip().split("\n")
    splits = [index - 1 for index, op in enumerate(operators) if op != " "]
    parts = [
        [number[i + 1 : j] for i, j in zip(splits, splits[1:] + [None])]
        for number in numbers
    ]
    return list(zip(zip(*parts), operators.split()))
```

so you just find where the splits are from the operators, make the parts by splitting at those locations (using zip to do a sliding window over the splits) and then use the zip trick to transpose the numbers so that theyre in the correct columns and then you can zip that collection with the operators.

by now you'll probably never want to see the zip function again.

now it isn't too disimilar to the first part.

```py
def parse_column_part_2(x: tuple[tuple[str, ...], str]):
    return [
        int("".join(number)) for number in zip_longest(*x[0], fillvalue=" ")
    ], add if x[1] == "+" else mul
```

to parse the column into integers, first you'll want to zip_longest so that you're reading down the columns for the individual numbers instead of across the rows. i.e.

```
123    1__
_45 -> 24_
__6    356
```

zip_longest is used here instead of zip because we're only keeping the leading spaces, not the trailing ones. this way, when it should have a trailing space, instead of immediately stopping it'll keep going until all collections are exhausted.

then you can just turn those numbers into integers and run the same kind of reduce as in part 1.

```py
def part_2():
    return sum(
        reduce(op, numbers)
        for numbers, op in list(map(parse_column_part_2, format_input()))
    )
```

this code is literally identical to part 1's function but using `parse_column_part_2` instead of `parse_column_part_1`
