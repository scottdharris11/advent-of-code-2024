"""utility imports"""
from utilities.data import read_lines
from utilities.runner import runner

@runner("Day 20", "Part 1")
def solve_part1(lines: list[str]) -> int:
    """part 1 solving function"""
    return 0

@runner("Day 20", "Part 2")
def solve_part2(lines: list[str]) -> int:
    """part 2 solving function"""
    return 0

# Data
data = read_lines("input/day20/input.txt")
sample = """""".splitlines()

# Part 1
assert solve_part1(sample) == 0
assert solve_part1(data) == 0

# Part 2
assert solve_part2(sample) == 0
assert solve_part2(data) == 0
