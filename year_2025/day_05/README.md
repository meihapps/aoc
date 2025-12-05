# day 5: cafeteria

this is an intervals question. there isn't really much more to say.

## formatting

formatting here is a little ugly because the input is multipart.

```py
with open("sample_input.txt" if sample else "input.txt") as file:
    ranges, ids = file.read().strip().split("\n\n")

return sorted(
    [tuplify_range(r) for r in ranges.strip().split("\n")]
), [int(id) for id in ids.strip().split("\n")]
```

first split it into the 2 parts so they can be handled separately.
part 2 is easy, just split on newline and convert to ints.

part 1 is slightly more involved, got a little helper function just to make it a little cleaner:

```py
def tuplify_range(r: str):
    a, b = r.split("-")
    return int(a), int(b)
```

the helper function turns the range strings into integer tuples and then that's just applied to each of them.

## part 1

for part 1 we only need to establish if numbers are in any of the intervals.

for that there are a couple components:
- turn all of those intervals into functions. the problem is a little easier when you can determine if something's in an interval by calling the interval with it.
- apply each of those intervals to your number. if any of them return true, that number passes.

### making the functions

```py
def make_range_funcs(ranges: list[tuple[int, int]]):
    return list(map(make_range_lambda, ranges))
```

this is just iterating over each of the ranges and turning them into an anonymous function with this helper function:

```py
def make_range_lambda(range: tuple[int, int]) -> Callable[[int], bool]:
    return lambda n: range[0] <= n <= range[1]
```

which just creates an anonymous function that has hardcoded values for the comparison. i didn't expect to have to make this a separate function but python has some strange scoping rules with anonymous functions so you want them to be the only thing in their scope really.

### applying them

```py
def part_1():
    ranges, ids = format_input()
    return len([id for id in ids if any(func(id) for func in make_range_funcs(ranges))])
```

just a little nested list comprehension, basically equivalent to:

```py
count = 0
for id in ids:
    for func in make_range_funcs(ranges)
        if func(id):
            count += 1
            break
```

but without looking like... that.

## part 2

this is where things get annoying, because now we want to find out how many numbers the ranges cover.

the naive solution would be to just take the sum of upper limits and subtract the sum of lower limits and then add how many limits there are.
i.e.
```
1-4
7-10
12-15

4 + 10 + 15 = 29
1 + 7 + 12 = 20
29 - 20 + 3 = 12

1,2,3,4,7,8,9,10,12,13,14,15 - 12 items
```

and this would work perfectly if not for the possibility of intervals overlapping.

the naive solution for the issue of overlapping intervals is to just make a list of all of the numbers in those intervals and deduplicate them but that is very unperformant, especially when our numbers are in the quadrillions - memory constraints and all that.

### merging intervals

merging intervals makes this much easier. if you have 2 intervals that overlap you can just turn them into one interval.
i.e.
```
1-7
5-9

min(1,5)-max(7,9)
1-9
```

and if we sort the intervals beforehand, we can forego the min check.

```py
def part_2_prime(acc: list[tuple[int, int]], x: tuple[int, int]):
    return (
        [x]
        if not acc
        else acc[:-1] + [(acc[-1][0], max(acc[-1][1], x[1]))]
        if x[0] <= acc[-1][1]
        else acc + [x]
    )
```

this here is our code solution for this. if we overlap with the last interval, merge them and if we don't, append the new interval instead.
the `[x] if not acc` is just there to account for when `acc` is empty (right at the start)

and now that the intervals are non-overlapping we can just add up the interval ranges:

```py
def get_range_length(r: tuple[int, int]):
    return r[1] - r[0] + 1

def part_2():
    return sum(map(get_range_length, reduce(part_2_prime, format_input()[0], [])))
```
