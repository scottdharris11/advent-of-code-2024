"""utility imports"""
from typing import Tuple
from utilities.data import read_lines
from utilities.runner import runner

@runner("Day 10", "Part 1")
def solve_part1(grid: list[str]):
    """part 1 solving function"""
    trails = 0
    for y, row in enumerate(grid):
        for x, col in enumerate(row):
            if col == '0':
                reached = set()
                path = list()
                path.append((x, y))
                follow_path(grid, path, reached, list())
                trails += len(reached)
    return trails

@runner("Day 10", "Part 2")
def solve_part2(grid: list[str]):
    """part 2 solving function"""
    trails = 0
    for y, row in enumerate(grid):
        for x, col in enumerate(row):
            if col == '0':
                paths = list()
                path = list()
                path.append((x, y))
                follow_path(grid, path, set(), paths)
                trails += len(paths)
    return trails

def follow_path(grid: list[str], path: list[Tuple[int, int]], reached: set[int, int], paths: list[list[Tuple[int, int]]]):
    """follow path to discover reached heights using valid moves"""
    moves = potential_moves(grid, path[-1])
    for move in moves:
        npath = list(path)
        npath.append(move)
        if grid[move[1]][move[0]] == '9':
            reached.add(move)
            paths.append(npath)
        else:
            follow_path(grid, npath, reached, paths)

def potential_moves(grid: list[str], loc: Tuple[int, int]) -> list[Tuple[int, int]]:
    """determine potential moves from current location"""
    height = len(grid)
    width = len(grid[0])
    moves = []
    current = int(grid[loc[1]][loc[0]])
    for d in [(1,0),(-1,0),(0,1),(0,-1)]:
        x = loc[0] + d[0]
        y = loc[1] + d[1]
        if x < 0 or x >= width or y < 0 or y >= height:
            continue
        if grid[y][x] == '.':
            continue
        if current + 1 == int(grid[y][x]):
            moves.append((x, y))
    return moves

# Data
data = read_lines("input/day10/input.txt")
sample = """0123
1234
8765
9876""".splitlines()
sample2 = """...0...
...1...
...2...
6543456
7.....7
8.....8
9.....9""".splitlines()
sample3 = """..90..9
...1.98
...2..7
6543456
765.987
876....
987....""".splitlines()
sample4 = """10..9..
2...8..
3...7..
4567654
...8..3
...9..2
.....01""".splitlines()
sample5 = """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732""".splitlines()

# Part 1
assert solve_part1(sample) == 1
assert solve_part1(sample2) == 2
assert solve_part1(sample3) == 4
assert solve_part1(sample4) == 3
assert solve_part1(sample5) == 36
assert solve_part1(data) == 535

# Part 2
sample6 = """.....0.
..4321.
..5..2.
..6543.
..7..4.
..8765.
..9....""".splitlines()
sample7 = """..90..9
...1.98
...2..7
6543456
765.987
876....
987....""".splitlines()
sample8 = """012345
123456
234567
345678
4.6789
56789.""".splitlines()

assert solve_part2(sample6) == 3
assert solve_part2(sample7) == 13
assert solve_part2(sample8) == 227
assert solve_part2(sample5) == 81
assert solve_part2(data) == 1186
