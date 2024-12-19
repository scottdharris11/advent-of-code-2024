"""utility imports"""
from utilities.data import read_lines
from utilities.runner import runner

@runner("Day 19", "Part 1")
def solve_part1(lines: list[str]) -> int:
    """part 1 solving function"""
    patterns_by_len, max_pattern_len = parse_patterns(lines[0])
    designs = lines[2:]
    valid = 0
    for design in designs:
        if possible(design, patterns_by_len, max_pattern_len):
            valid += 1
    return valid

@runner("Day 19", "Part 2")
def solve_part2(lines: list[str]) -> int:
    """part 2 solving function"""
    patterns_by_len, max_pattern_len = parse_patterns(lines[0])
    designs = lines[2:]
    total = 0
    for design in designs:
        total += arrangements(design, patterns_by_len, max_pattern_len)
    return total

def memoize_possible(f):
    """function to remember function call results for possible"""
    memo = {}
    def helper(m: str, p, mp):
        if (m) not in memo:
            memo[m] = f(m, p, mp)
        return memo[m]
    return helper

@memoize_possible
def possible(design: str, patterns: dict[int,set[str]], max_pattern: int) -> bool:
    """recursive function to determine if design is possible given patterns"""
    dl = len(design)
    m = max(max_pattern,dl)
    for l in range(1, m+1, 1):
        pbl = patterns.get(l, None)
        if pbl is None:
            continue
        dpc = design[:l]
        if dpc in pbl:
            if l == dl:
                return True
            if possible(design[l:], patterns, max_pattern):
                return True
    return False

def memoize_arrangements(f):
    """function to remember function call results for arrangements"""
    memo = {}
    def helper(m: str, p, mp):
        if (m) not in memo:
            memo[m] = f(m, p, mp)
        return memo[m]
    return helper

@memoize_arrangements
def arrangements(design: str, patterns: dict[int,set[str]], max_pattern: int) -> int:
    """recursive function to determine if design is possible given patterns"""
    dl = len(design)
    m = max(max_pattern,dl)
    arranges = 0
    for l in range(1, m+1, 1):
        pbl = patterns.get(l, None)
        if pbl is None:
            continue
        dpc = design[:l]
        if dpc in pbl:
            if l == dl:
                arranges += 1
            else:
                arranges += arrangements(design[l:], patterns, max_pattern)
    return arranges

def parse_patterns(line: str) -> tuple[dict[int,set[str]], int]:
    """parse set of patterns from input"""
    patterns = {}
    max_len = 0
    for pattern in line.split(", "):
        l = len(pattern)
        pbl = patterns.get(l, set())
        pbl.add(pattern)
        patterns[l] = pbl
        max_len = max(max_len, l)
    return patterns, max_len

# Data
data = read_lines("input/day19/input.txt")
sample = """r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb""".splitlines()

# Part 1
assert solve_part1(sample) == 6
assert solve_part1(data) == 287

# Part 2
assert solve_part2(sample) == 16
assert solve_part2(data) > 545103755682737
