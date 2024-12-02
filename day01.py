"""utility imports"""
from utilities.data import read_lines
from utilities.runner import runner

@runner("Day 1", "Part 1")
def solve_part1(lines: list):
    """part 1 solving function"""
    left, right = digits(lines)
    left.sort()
    right.sort()
    total = 0
    for i, l in enumerate(left):
        total += abs(l - right[i])
    return total

@runner("Day 1", "Part 2")
def solve_part2(lines: list):
    """part 2 solving function"""
    left, right = digits(lines)
    rightd = {}
    for d in right:
        rightd[d] = rightd.get(d, 0) + 1
    total = 0
    for d in left:
        total += d * rightd.get(d, 0)
    return total

def digits(lines: list):
    """build set of digit lists from input lines"""
    left = []
    right = []
    for line in lines:
        s = line.split("   ")
        left.append(int(s[0]))
        right.append(int(s[1]))
    return left, right

# Data
data = read_lines("input/day01/input.txt")
sample = [
    "3   4",
    "4   3",
    "2   5",
    "1   3",
    "3   9",
    "3   3",
]

# Part 1
assert solve_part1(sample) == 11
assert solve_part1(data) == 1530215

# Part 2
assert solve_part2(sample) == 31
assert solve_part2(data) == 26800609
