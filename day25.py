"""utility imports"""
from utilities.data import read_lines
from utilities.runner import runner

@runner("Day 25", "Part 1")
def solve_part1(lines: list[str]) -> int:
    """part 1 solving function"""
    locks, keys = parse_schematics(lines)
    fit = 0
    for lock in locks:
        for key in keys:
            if will_fit(key, lock):
                fit += 1
    return fit

def parse_schematics(lines: list[str]) -> tuple[list[list[int]], list[list[int]]]:
    """parse set of locks and keys from input"""
    locks = []
    keys = []
    for i in range(7,len(lines)+1,8):
        if lines[i-7][0] == '#':
            locks.append(build_lock(lines[i-7:i]))
        else:
            keys.append(build_key(lines[i-7:i]))
    return locks, keys

def build_lock(lines: list[str]) -> list[int]:
    """build lock from schematics"""
    heights = []
    for c in range(5):
        r = 0
        while True:
            if lines[r][c] == '.':
                break
            r += 1
        heights.append(r-1)
    return heights

def build_key(lines: list[str]) -> list[int]:
    """build key from schematics"""
    heights = []
    for c in range(5):
        r = 0
        i = 6
        while True:
            if lines[i][c] == '.':
                break
            r += 1
            i -= 1
        heights.append(r-1)
    return heights

def will_fit(key: list[int], lock: list[int]) -> bool:
    """determine if the supplied key will fit the supplied lock"""
    for i, kv in enumerate(key):
        if kv + lock[i] >= 6:
            return False
    return True

# Data
data = read_lines("input/day25/input.txt")
sample = """#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####
""".splitlines()

# Part 1
assert solve_part1(sample) == 3
assert solve_part1(data) == 2691
