"""utility imports"""
from typing import Set, Tuple
from utilities.data import read_lines
from utilities.runner import runner

directions = [(0,-1),(1,0),(0,1),(-1,0)]

@runner("Day 6", "Part 1")
def solve_part1(grid: list[str]):
    """part 1 solving function"""
    loc = find_guard(grid)
    height = len(grid)
    width = len(grid[0])
    
    d = 0
    visited = set()
    visited.add(loc)
    visited_in_dir = set()
    while True:
        visited_in_dir.add(loc + directions[d])
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
    loc = find_guard(grid)
    height = len(grid)
    width = len(grid[0])

    d = 0
    visited = set()
    visited.add(loc)
    visited_in_dir = set()
    loop_points = 0
    while True:
        visited_in_dir.add(loc + directions[d])
        if turn_into_loop(grid, loc, d, visited_in_dir, visited):
            loop_points += 1
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
    return loop_points

def find_guard(grid: list[str]) -> Tuple[int, int]:
    """find position of guard on grid"""
    for y, row in enumerate(grid):
        for x, col in enumerate(row):
            if col == '^':
                return ((x, y))

def turn_into_loop(grid: list[str], loc: Tuple[int,int], d: int, vid: Set, visited: Set) -> bool:
    """
    determine if putting a turn at the path point ahead would trigger loop
    by checking to see if a path in that direction has already been followed.
    """
    height = len(grid)
    width = len(grid[0])
    place_point = (loc[0]+directions[d][0],loc[1]+directions[d][1])
    
    # outside grid
    if place_point[0] < 0 or place_point[0] >= width:
        return False
    if place_point[1] < 0 or place_point[1] >= height:
        return False
    # already something there
    if grid[place_point[1]][place_point[0]] in ['#','^']:
        return False
    # visited on path already so not eligible since it would change the path to get here
    if place_point in visited:
        return False

    vid = vid.copy()
    d += 1
    if d >= len(directions):
        d = 0
    while True:
        loc = (loc[0]+directions[d][0],loc[1]+directions[d][1])
        if loc[0] < 0 or loc[0] >= width:
            return False
        if loc[1] < 0 or loc[1] >= height:
            return False
        if grid[loc[1]][loc[0]] == '#':
            loc = (loc[0]-directions[d][0],loc[1]-directions[d][1])
            d += 1
            if d >= len(directions):
                d = 0
        loc_in_dir = loc + directions[d]
        if loc_in_dir in vid:
            return True
        vid.add(loc + directions[d])

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
assert solve_part2(sample) == 6
assert solve_part2(data) == 0
