from utilities.data import read_lines, parse_integers
from utilities.runner import Runner

@Runner("Day 2", "Part 1")
def solve_part1(lines: list):
    safe = 0
    for line in lines:
        report = parse_integers(line, " ")
        if safe_report(report):
            safe += 1
    return safe

@Runner("Day 2", "Part 2")
def solve_part2(lines: list):
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
    inc = report[1] > report[0]
    for i in range(1,len(report)):
        if not safe_level(inc, report[i-1], report[i]):
            return False
    return True

def safe_level(inc: bool, prev: int, current: int):
    if inc and current <= prev:
        return False
    elif not inc and current >= prev:
        return False
    if abs(current-prev) > 3:
        return False
    return True

# Part 1
input = read_lines("input/day02/input.txt")
sample = [
    "7 6 4 2 1",
    "1 2 7 8 9",
    "9 7 6 2 1",
    "1 3 2 4 5",
    "8 6 4 4 1",
    "1 3 6 7 9",
]

value = solve_part1(sample)
assert(value == 2)
value = solve_part1(input)
assert(value == 287)

# Part 2
value = solve_part2(sample)
assert(value == 4)
value = solve_part2(input)
assert(value == 354)
