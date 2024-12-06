"""utility imports"""
from typing import Tuple
from utilities.data import read_lines
from utilities.runner import runner

directions = [(0,-1),(1,0),(0,1),(-1,0)]

@runner("Day 6", "Part 1")
def solve_part1(grid: list[str]):
    """part 1 solving function"""
    loc = find_guard(grid)
    height = len(grid)
    width = len(grid[0])
    visited = set()
    visited.add(loc)
    d = 0
    while True:
        loc = (loc[0]+directions[d][0],loc[1]+directions[d][1])
        if loc[0] < 0 or loc[0] >= width:
            break
        if loc[1] < 0 or loc[1] >= height:
            break
        if grid[loc[1]][loc[0]] == '#':
            loc = (loc[0]-directions[d][0],loc[1]-directions[d][1])
            d += 1
            if d >= len(directions):
                d = 0
        visited.add(loc)
    return len(visited)

@runner("Day 6", "Part 2")
def solve_part2(grid: list[str]):
    """part 2 solving function"""
    return 0

def find_guard(grid: list[str]) -> Tuple[int, int]:
    """find position of guard on grid"""
    for y, row in enumerate(grid):
        for x, col in enumerate(row):
            if col == '^':
                return ((x, y))

# Data
data = read_lines("input/day06/input.txt")
sample = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
""".splitlines()

# Part 1
assert solve_part1(sample) == 41
assert solve_part1(data) == 4656

# Part 2
assert solve_part2(sample) == 0
assert solve_part2(data) == 0
