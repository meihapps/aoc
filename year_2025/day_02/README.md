# day 2: gift shop

this one's premise is that you have a bunch of numerical ranges (inclusive-inclusive) and some of the numbers in those ranges meet some arbitrary conditions. you need to find all of those numbers.

of course, to start you always format your inputs so you can work with them.

```py
with open("sample_input.txt" if sample else "input.txt") as file:
    return (
        range(int(start), int(end) + 1)
        for start, end in findall(r"(\d+)-(\d+)", file.read())
    )
```

this is simply turning those strings into python ranges, remembering to add 1 to the end values because python ranges are inclusive-exclusive (the only valid way to do a range)

## part 1

the conditions for a number here are quite simple. the first half of the number has to be the same as the last half of the number. this means that we're only looking at numbers with even digits.
the output here is formatted as a sum of the numbers that met the conditions, so here's the code for that:

```py
sum(
    [
        n
        for r in format_input()
        for n in r
        if not len(str(n)) % 2
        and str(n)[: len(str(n)) // 2] == str(n)[len(str(n)) // 2 :]
    ]
)
```

quite simply just filtering out the numbers with an odd number of digits, and then the ones that don't have the same first and last half and summing them.

## part 2

this is mostly the same, however instead of being half and half, the number can be split into any number of evenly sized groups and all groups need to be the same.

there are going to be a few key components to doing this task:

- splitting the number into a variable number of equally sized chunks
- taking some chunks and seeing if they're all equal
- seeing if a number has any valid way to split it based on these conditions
- summing all those numbers that meet the conditions

### splitting into equally sized chunks

here we can use a fun little zip trick ! this is a little esoteric but basically we're kinda tricking the list multiplication operation into going through the string `len(string) // parts` items at a time.
this works because iterators consume values when used, so each time it tries to make another copy it ends up cycling one character further through string. once you understand that trick the rest kind of just falls into place.

```py
zip(*[iter(string)] * (len(string) // parts))
```

### ensuring all chunks are equal

this is relatively trivial, but i'm putting it as it's own separate function because there's no nice way to do it honestly.
you have to do an assignment that feels unnecessary - and i dont want additional lines in my main logic just because of a silly assignment, so it's separated out to keep that main loop clean.

this is 100% a purely stylistic choice and certainly isn't contributing to the complexity of the problem, but if i'm separating it out i should probably still explain myself.

```py
head = l[0]
return all(i == head for i in l)
```

get the first element. make sure all the elements equal it. very simple.

### try all splits for validity

this is just an iterative problem. we need to try all of them so we do.

```py
any(
    all_same(list(chunkify(str(n), d)))
    for d in range(2, len(str(n)) + 1)
    if not len(str(n)) % d
)
```

it's just checking if any number of splits is good for the number provided - the actual amount doesn't matter so we discard that and leave it as a boolean.

### sum those numbers

sum the numbers that pass the filter we just made. there's our solution.

```py
sum(n for r in format_input() for n in r if part_2_helper(n))
```
