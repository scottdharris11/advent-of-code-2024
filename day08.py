"""utility imports"""
from typing import Tuple
from utilities.data import read_lines
from utilities.runner import runner

@runner("Day 8", "Part 1")
def solve_part1(grid: list[str]):
    """part 1 solving function"""
    pairs = antenna_pairs(parse_antennas(grid))
    height = len(grid)
    width = len(grid[0])
    unique_nodes = set()
    for pair in pairs:
        nodes = pair.antinodes(width, height)
        unique_nodes.update(nodes)
    return len(unique_nodes)

@runner("Day 8", "Part 2")
def solve_part2(grid: list[str]):
    """part 2 solving function"""
    pairs = antenna_pairs(parse_antennas(grid))
    height = len(grid)
    width = len(grid[0])
    unique_nodes = set()
    for pair in pairs:
        nodes = pair.antinodes_with_resonate(width, height)
        unique_nodes.update(nodes)
    return len(unique_nodes)

class Antenna:
    """antenna freqeuncy and location"""
    def __init__(self, frequency: str, x: int, y: int) -> None:
        self.frequency = frequency
        self.x = x
        self.y = y

    def __repr__(self):
        return str((self.frequency, self.x, self.y))

    def __eq__(self, other):
        if not isinstance(other, Antenna):
            return False
        return self.frequency == other.frequency and self.x == other.x and self.y == other.y

class AntennaPair:
    """pair of antennas"""
    def __init__(self, a: Antenna, b: Antenna) -> None:
        self.a = a
        self.b = b
        self.slope = (a.x - b.x, a.y - b.y)

    def __repr__(self):
        return str((self.a, self.b, self.slope))

    def antinodes(self, max_x: int, max_y: int) -> set[Tuple[int,int]]:
        """antinodes produced by the pair within supplied grid"""
        nodes = set()
        pnode = (self.a.x + self.slope[0], self.a.y + self.slope[1])
        if pnode[0] >= 0 and pnode[0] < max_x and pnode[1] >= 0 and pnode[1] < max_y:
            nodes.add(pnode)
        pnode = (self.b.x - self.slope[0], self.b.y - self.slope[1])
        if pnode[0] >= 0 and pnode[0] < max_x and pnode[1] >= 0 and pnode[1] < max_y:
            nodes.add(pnode)
        return nodes

    def antinodes_with_resonate(self, max_x: int, max_y: int) -> set[Tuple[int,int]]:
        """resonated antinodes produced by the pair within supplied grid"""
        loc = (self.a.x, self.a.y)
        nodes = set()
        nodes.add(loc)
        while True:
            loc = (loc[0] + self.slope[0], loc[1] + self.slope[1])
            if loc[0] < 0 or loc[0] >= max_x or loc[1] < 0 or loc[1] >= max_y:
                break
            nodes.add(loc)
        loc = (self.a.x, self.a.y)
        while True:
            loc = (loc[0] - self.slope[0], loc[1] - self.slope[1])
            if loc[0] < 0 or loc[0] >= max_x or loc[1] < 0 or loc[1] >= max_y:
                break
            nodes.add(loc)
        return nodes

def parse_antennas(grid: list[str]) -> dict[str,Antenna]:
    """parse antennas from the grid"""
    by_freq = {}
    for y, row in enumerate(grid):
        for x, col in enumerate(row):
            if col != '.':
                a = Antenna(col, x, y)
                l = by_freq.get(a.frequency, [])
                l.append(a)
                by_freq[a.frequency] = l
    return by_freq

def antenna_pairs(by_freq: dict[str,list[Antenna]]) -> list[AntennaPair]:
    """build set of unique antenna pairs"""
    pairs = []
    for freqs in by_freq.items():
        for i, a in enumerate(freqs[1]):
            for b in freqs[1][i+1:]:
                if a != b:
                    pairs.append(AntennaPair(a, b))
    return pairs

# Data
data = read_lines("input/day08/input.txt")
sample = """............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............""".splitlines()

sample2 = """T.........
...T......
.T........
..........
..........
..........
..........
..........
..........
..........""".splitlines()

# Part 1
assert solve_part1(sample) == 14
assert solve_part1(data) == 285

# Part 2
assert solve_part2(sample2) == 9
assert solve_part2(sample) == 34
assert solve_part2(data) == 944
