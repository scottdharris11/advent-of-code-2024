"""utility imports"""
from utilities.data import read_lines
from utilities.runner import runner

@runner("Day 7", "Part 1")
def solve_part1(lines: list[str]):
    """part 1 solving function"""
    valid = 0
    for line in lines:
        test, values = parse(line)
        if equation_valid(0, test, values, 0, len(values), ['+', '*']):
            valid += test
    return valid

@runner("Day 7", "Part 2")
def solve_part2(lines: list[str]):
    """part 2 solving function"""
    valid = 0
    for line in lines:
        test, values = parse(line)
        if equation_valid(0, test, values, 0, len(values), ['+', '*', '|']):
            valid += test
    return valid

def parse(line: str) -> tuple[int, list[int]]:
    """parse input line"""
    idx = line.index(":")
    test = int(line[:idx])
    values = list(map(int, line[idx+1:].strip().split(" ")))
    return test, values

def equation_valid(start: int, test: int, vals: list[int], idx: int, end: int, ops: list[chr]) -> bool:
    """recursively compute until complete and validate against test"""
    if idx == end or start > test:
        return start == test
    val = vals[idx]
    for op in ops:
        if op == '+':
            if equation_valid(start + val, test, vals, idx+1, end, ops):
                return True
        elif op == '*' and start > 0:
            if equation_valid(start * val, test, vals, idx+1, end, ops):
                return True
        elif op == '|':
            if start == 0:
                continue
            if equation_valid(int(str(start)+str(val)), test, vals, idx+1, end, ops):
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
assert solve_part2(sample) == 11387
assert solve_part2(data) == 59002246504791
