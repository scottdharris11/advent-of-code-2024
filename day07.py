"""utility imports"""
from typing import Tuple
from utilities.data import read_lines
from utilities.runner import runner

@runner("Day 7", "Part 1")
def solve_part1(lines: list[str]):
    """part 1 solving function"""
    valid = 0
    for line in lines:
        test, values = parse(line)
        if equation_valid(0, test, values):
            valid += test
    return valid

@runner("Day 7", "Part 2")
def solve_part2(lines: list[str]):
    """part 2 solving function"""
    return 0

def parse(line: str) -> Tuple[int, list[int]]:
    """parse input line"""
    idx = line.index(":")
    test = int(line[:idx])
    values = list(map(int, line[idx+1:].strip().split(" ")))
    return test, values

def equation_valid(start: int, test: int, values: list[int]) -> bool:
    """recursively compute until complete and validate against test"""
    val = values[0]
    if len(values) == 1:
        return (start + val) == test or (start * val) == test
    else:
        if equation_valid(start + val, test, values[1:]):
            return True
        if equation_valid(start * val, test, values[1:]):
            return True
        return False

# Data
data = read_lines("input/day07/input.txt")
sample = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20""".splitlines()

# Part 1
assert solve_part1(sample) == 3749
assert solve_part1(data) == 6083020304036

# Part 2
assert solve_part2(sample) == 0
assert solve_part2(data) == 0
