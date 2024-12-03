"""utility imports"""
import re
from utilities.data import read_lines
from utilities.runner import runner

@runner("Day 3", "Part 1")
def solve_part1(lines: list):
    """part 1 solving function"""
    extract = re.compile(r'mul\(([0-9]{1,3}),([0-9]{1,3})\)')
    total = 0
    for line in lines:
        matches = extract.finditer(line)
        for match in matches:
            total += int(match.group(1)) * int(match.group(2))
    return total

@runner("Day 3", "Part 2")
def solve_part2(lines: list):
    """part 2 solving function"""
    extract = re.compile(r'mul\(([0-9]{1,3}),([0-9]{1,3})\)|do\(\)|don\'t\(\)')
    total = 0
    on = True
    for line in lines:
        matches = extract.finditer(line)
        for match in matches:
            if match.group(0) == "do()":
                on = True
            elif match.group(0) == "don't()":
                on = False
            elif on:
                total += int(match.group(1)) * int(match.group(2))
    return total

# Data
data = read_lines("input/day03/input.txt")
sample = ["xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"]
sample2 = ["xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"]

# Part 1
assert solve_part1(sample) == 161
assert solve_part1(data) == 184122457

# Part 2
assert solve_part2(sample2) == 48
assert solve_part2(data) == 107862689
