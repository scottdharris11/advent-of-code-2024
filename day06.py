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
    while True:
        loc = tuple(x + y for x, y in zip(loc, directions[d]))
        if loc[0] < 0 or loc[0] >= width or loc[1] < 0 or loc[1] >= height:
            break
        if grid[loc[1]][loc[0]] == '#':
            loc = tuple(x - y for x, y in zip(loc, directions[d]))
            d = turn(d)
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
        loc = tuple(x + y for x, y in zip(loc, directions[d]))
        if loc[0] < 0 or loc[0] >= width or loc[1] < 0 or loc[1] >= height:
            break
        if grid[loc[1]][loc[0]] == '#':
            loc = tuple(x - y for x, y in zip(loc, directions[d]))
            d = turn(d)
        visited.add(loc)
    return loop_points

def find_guard(grid: list[str]) -> Tuple[int, int]:
    """find position of guard on grid"""
    for y, row in enumerate(grid):
        for x, col in enumerate(row):
            if col == '^':
                return ((x, y))

def turn(current: int) -> int:
    """turn direction"""
    d = current + 1
    if d >= len(directions):
        d = 0
    return d

def turn_into_loop(grid: list[str], loc: Tuple[int,int], d: int, vid: Set, visited: Set) -> bool:
    """
    determine if putting a turn at the path point ahead would trigger loop
    by checking to see if a path in that direction has already been followed.
    """
    height = len(grid)
    width = len(grid[0])
    point = tuple(x + y for x, y in zip(loc, directions[d]))

    # outside grid
    if point[0] < 0 or point[0] >= width or point[1] < 0 or point[1] >= height:
        return False
    # already something there
    if grid[point[1]][point[0]] in ['#','^']:
        return False
    # visited on path already so not eligible since it would change the path to get here
    if point in visited:
        return False

    # turn and then process until either getting out (no loop)
    # or a path already used is entered (indicating loop)
    d = turn(d)
    vid = vid.copy()
    while True:
        loc = tuple(x + y for x, y in zip(loc, directions[d]))
        if loc[0] < 0 or loc[0] >= width or loc[1] < 0 or loc[1] >= height:
            return False
        if grid[loc[1]][loc[0]] == '#' or loc == point:
            loc = tuple(x - y for x, y in zip(loc, directions[d]))
            d = turn(d)
        loc_in_dir = loc + directions[d]
        if loc_in_dir in vid:
            return True
        vid.add(loc_in_dir)

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
assert solve_part2(data) == 1575
