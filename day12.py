"""utility imports"""
from utilities.data import read_lines
from utilities.runner import runner

@runner("Day 12", "Part 1")
def solve_part1(grid: list[str]):
    """part 1 solving function"""
    fence_cost = 0
    for r in plant_regions(grid):
        fence_cost += r.cost(grid)
    return fence_cost

@runner("Day 12", "Part 2")
def solve_part2(grid: list[str]):
    """part 2 solving function"""
    fence_cost = 0
    for r in plant_regions(grid):
        fence_cost += r.bulk_cost(grid)
    return fence_cost

class Region:
    """plant region definition"""
    def __init__(self, plant: chr, start: tuple[int,int]) -> None:
        self.plant = plant
        self.plots = set()
        self.plots.add(start)
        self.fence_sides = set()

    def __repr__(self):
        return str(self.plant) + ": " + str(self.plots)

    def cost(self, grid: list[str]) -> int:
        """calculate the cost of the region"""
        return len(self.plots) * len(self.perimeter(grid))

    def bulk_cost(self, grid: list[str]) -> int:
        """calculate the bulk cost of the region by finding all the sides"""
        self.perimeter(grid)
        sides = 0
        for d in [(1,0),(-1,0),(0,1),(0,-1)]:
            # find the perimeter points by each type of side (left,right,top,bottom)
            # and then sort the points to find the contiguous points which are a side
            ps = self.__sides_in_direction__(d)
            for v in ps.values():
                v.sort()
                sides += 1
                for i in range(len(v)-1):
                    if v[i+1] != v[i]+1:
                        sides += 1
        return len(self.plots) * sides

    def perimeter(self, grid: list[str]) -> set[tuple[tuple[int,int],tuple[int,int]]]:
        """detremine the perimeter sides of the region"""
        height = len(grid)
        width = len(grid[0])
        for plot in self.plots:
            for d in [(1,0),(-1,0),(0,1),(0,-1)]:
                x = plot[0] + d[0]
                y = plot[1] + d[1]
                if x < 0 or x >= width or y < 0 or y >= height:
                    self.fence_sides.add((plot, d))
                elif (x, y) not in self.plots:
                    self.fence_sides.add((plot, d))
        return self.fence_sides

    def __sides_in_direction__(self, direction: tuple[int,int]) -> dict[int,list[int]]:
        """find the points that have perimeter sides"""
        edges = {}
        for fs in self.fence_sides:
            if fs[1] == direction:
                k, v = 0, 0
                if direction[0] == 0:
                    v, k = map(int,fs[0])
                else:
                    k, v = map(int,fs[0])
                edges[k] = edges.get(k,[])
                edges[k].append(v)
        return edges

def plant_regions(grid: list[str]) -> list[Region]:
    """identify the distinct plant regions in the grid"""
    assigned = set()
    regions = []
    for y, row in enumerate(grid):
        for x, col in enumerate(row):
            if (x,y) in assigned:
                continue
            region = Region(col, (x,y))
            plant_region(grid, col, (x,y), region.plots, assigned)
            regions.append(region)
    return regions

def plant_region(grid: list[str], plant: chr, last: tuple[int,int], region: set[tuple[int, int]], prev: set[tuple[int, int]]):
    """follow grid to find connected plants of same type"""
    moves = potential_moves(grid, plant, last, prev)
    for move in moves:
        region.add(move)
        prev.add(move)
        plant_region(grid, plant, move, region, prev)

def potential_moves(grid: list[str], plant: chr, loc: tuple[int, int], prev: set[tuple[int, int]]) -> list[tuple[int, int]]:
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
sample4 = """EEEEE
EXXXX
EEEEE
EXXXX
EEEEE""".splitlines()
sample5 = """AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA""".splitlines()

# Part 1
assert solve_part1(sample) == 140
assert solve_part1(sample2) == 772
assert solve_part1(sample3) == 1930
assert solve_part1(data) == 1396562

# Part 2
assert solve_part2(sample) == 80
assert solve_part2(sample2) == 436
assert solve_part2(sample4) == 236
assert solve_part2(sample5) == 368
assert solve_part2(data) == 844132
