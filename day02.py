"""utility imports"""
from utilities.data import read_lines, parse_integers
from utilities.runner import runner

@runner("Day 2", "Part 1")
def solve_part1(lines: list):
    """part 1 solving function"""
    safe = 0
    for line in lines:
        report = parse_integers(line, " ")
        if safe_report(report):
            safe += 1
    return safe

@runner("Day 2", "Part 2")
def solve_part2(lines: list):
    """part 2 solving function"""
    safe = 0
    for line in lines:
        report = parse_integers(line, " ")
        if safe_report(report):
            safe += 1
        else:
            # check if safe if any one level is removed
            for i in range(len(report)):
                adjusted_report = report[:i] + report[i+1:]
                if safe_report(adjusted_report):
                    safe += 1
                    break
    return safe

def safe_report(report: list):
    """determine if the supplied report is safe"""
    inc = report[1] > report[0]
    for i in range(1,len(report)):
        if not safe_level(inc, report[i-1], report[i]):
            return False
    return True

def safe_level(inc: bool, prev: int, current: int):
    """determine if the current level is safe"""
    if inc and current <= prev:
        return False
    elif not inc and current >= prev:
        return False
    if abs(current-prev) > 3:
        return False
    return True

# Data
data = read_lines("input/day02/input.txt")
sample = [
    "7 6 4 2 1",
    "1 2 7 8 9",
    "9 7 6 2 1",
    "1 3 2 4 5",
    "8 6 4 4 1",
    "1 3 6 7 9",
]

# Part 1
assert solve_part1(sample) == 2
assert solve_part1(data) == 287

# Part 2
assert solve_part2(sample) == 4
assert solve_part2(data) == 354
