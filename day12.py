"""utility imports"""
from typing import Tuple
from utilities.data import read_lines
from utilities.runner import runner

@runner("Day 12", "Part 1")
def solve_part1(grid: list[str]):
    """part 1 solving function"""
    assigned = set()
    fence_cost = 0
    for y, row in enumerate(grid):
        for x, col in enumerate(row):
            if (x,y) in assigned:
                continue
            region = Region(col, (x,y))
            plant_region(grid, col, (x,y), region.plots, assigned)
            fence_cost += region.cost(grid)
    return fence_cost

@runner("Day 12", "Part 2")
def solve_part2(grid: list[str]):
    """part 2 solving function"""
    return 0

class Region:
    """plant region definition"""
    def __init__(self, plant: chr, start: Tuple[int,int]) -> None:
        self.plant = plant
        self.plots = set()
        self.plots.add(start)
        self.perm = 0

    def __repr__(self):
        return str(self.plant) + ": " + str(self.plots)

    def cost(self, grid: list[str]) -> int:
        """calculate the cost of the region"""
        return len(self.plots) * self.perimeter(grid)

    def perimeter(self, grid: list[str]) -> int:
        """calculate the permeter of the region"""
        if self.perm != 0:
            return self.perm
        height = len(grid)
        width = len(grid[0])
        for plot in self.plots:
            for d in [(1,0),(-1,0),(0,1),(0,-1)]:
                x = plot[0] + d[0]
                y = plot[1] + d[1]
                if x < 0 or x >= width or y < 0 or y >= height:
                    self.perm += 1
                elif (x, y) not in self.plots:
                    self.perm += 1
        return self.perm


def plant_region(grid: list[str], plant: chr, last: Tuple[int,int], region: set[Tuple[int, int]], prev: set[Tuple[int, int]]):
    """follow grid to find connected plants of same type"""
    moves = potential_moves(grid, plant, last, prev)
    for move in moves:
        region.add(move)
        prev.add(move)
        plant_region(grid, plant, move, region, prev)

def potential_moves(grid: list[str], plant: chr, loc: Tuple[int, int], prev: set[Tuple[int, int]]) -> list[Tuple[int, int]]:
    """determine potential moves from current location"""
    height = len(grid)
    width = len(grid[0])
    moves = []
    for d in [(1,0),(-1,0),(0,1),(0,-1)]:
        x = loc[0] + d[0]
        y = loc[1] + d[1]
        if x < 0 or x >= width or y < 0 or y >= height:
            continue
        if grid[y][x] != plant:
            continue
        if (x,y) in prev:
            continue
        moves.append((x, y))
    return moves

# Data
data = read_lines("input/day12/input.txt")
sample = """AAAA
BBCD
BBCC
EEEC""".splitlines()
sample2 = """OOOOO
OXOXO
OOOOO
OXOXO
OOOOO""".splitlines()
sample3 = """RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE""".splitlines()

# Part 1
assert solve_part1(sample) == 140
assert solve_part1(sample2) == 772
assert solve_part1(sample3) == 1930
assert solve_part1(data) == 1396562

# Part 2
assert solve_part2(sample) == 0
assert solve_part2(data) == 0
