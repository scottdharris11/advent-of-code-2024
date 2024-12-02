from utilities.data import read_lines
from utilities.runner import Runner

@Runner("Day 1", "Part 1")
def solve_part1(lines: list):
    left, right = digits(lines)
    left.sort()
    right.sort()
    total = 0
    for i in range(len(left)):
        total += abs(left[i] - right[i])
    return total

@Runner("Day 1", "Part 2")
def solve_part2(lines: list):
    left, right = digits(lines)
    rightd = {}
    for d in right:
        rightd[d] = rightd.get(d, 0) + 1
    total = 0
    for d in left:
        total += d * rightd.get(d, 0)
    return total

def digits(lines: list):
    left = []
    right = []
    for line in lines:
        s = line.split("   ")
        left.append(int(s[0]))
        right.append(int(s[1]))
    return left, right

# Part 1
input = read_lines("input/day01/input.txt")
sample = [
    "3   4",
    "4   3",
    "2   5",
    "1   3",
    "3   9",
    "3   3",
]

value = solve_part1(sample)
assert(value == 11)
value = solve_part1(input)
assert(value == 1530215)

# Part 2
value = solve_part2(sample)
assert(value == 31)
value = solve_part2(input)
assert(value == 26800609)
