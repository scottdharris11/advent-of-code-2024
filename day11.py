"""utility imports"""
from collections import Counter
from utilities.data import parse_integers, read_lines
from utilities.runner import runner

@runner("Day 11", "Part 1")
def solve_part1(values: list[str], blinks: int):
    """part 1 solving function"""
    stones = dict(Counter(values))

    for _ in range(blinks):
        wstones = {}
        for n, count in stones.items():
            if n == 0:
                wstones[1] = wstones.get(1,0) + count
            elif len(str(n)) % 2 == 0:
                s = str(n)
                sidx = int(len(s) / 2)
                left = int(s[:sidx])
                right = int(s[sidx:])
                wstones[left] = wstones.get(left,0) + count
                wstones[right] = wstones.get(right,0) + count
            else:
                n2024 = n * 2024
                wstones[n2024] = wstones.get(n2024,0) + count
        stones = wstones

    return sum(stones.values())

# Data
data = parse_integers(read_lines("input/day11/input.txt")[0], " ")
sample = parse_integers("""125 17""", " ")

# Part 1
assert solve_part1(sample, 6) == 22
assert solve_part1(sample, 25) == 55312
assert solve_part1(data, 25) == 220999

# Part 2 (using part 1 for longer iteration)
assert solve_part1(data, 75) == 261936432123724