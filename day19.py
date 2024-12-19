"""utility imports"""
from utilities.data import read_lines
from utilities.runner import runner

@runner("Day 19", "Part 1")
def solve_part1(lines: list[str]) -> int:
    """part 1 solving function"""
    patterns_by_len = {}
    max_pattern_len = 0
    for pattern in lines[0].split(", "):
        l = len(pattern)
        pbl = patterns_by_len.get(l, set())
        pbl.add(pattern)
        patterns_by_len[l] = pbl
        if l > max_pattern_len:
            max_pattern_len = l
    designs = lines[2:]
    valid = 0
    for design in designs:
        if possible(design, patterns_by_len, max_pattern_len):
            valid += 1
    return valid

@runner("Day 19", "Part 2")
def solve_part2(lines: list[str]) -> int:
    """part 2 solving function"""
    return 0

def memoize(f):
    memo = {}
    def helper(m: str, p: list[int], d: int):
        t = tuple(p)
        if (m, t, d) not in memo:            
            memo[(m, t, d)] = f(m, p, d)
        return memo[(m, t, d)]
    return helper

@memoize
def possible(design: str, patterns_by_len: dict[int,set[str]], max_len: int) -> bool:
    """recursive function to determine if design is possible given patterns"""
    dl = len(design)
    m = max(max_len,dl)
    for l in range(1, m+1, 1):
        pbl = patterns_by_len.get(l, None)
        if pbl is None:
            continue
        dpc = design[:l]
        if dpc in pbl:
            if l == dl:
                return True
            if possible(design[l:], patterns_by_len, max_len):
                return True
    return False

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
assert solve_part2(sample) == 0
assert solve_part2(data) == 0
