"""utility imports"""
import functools
from utilities.data import read_lines
from utilities.runner import runner

@runner("Day 20", "Part 1")
def solve_part1(lines: list[str], min_save: int) -> int:
    """part 1 solving function"""
    return cheat_count(lines, min_save, 2)

@runner("Day 20", "Part 2")
def solve_part2(lines: list[str], min_save: int) -> int:
    """part 2 solving function"""
    return cheat_count(lines, min_save, 20)

def cheat_count(lines: list[str], min_save: int, cheat_steps: int) -> int:
    """find the number of cheats with the minimum supplied savings"""
    race = Race(lines)
    path = race.path()
    visited = set()
    cheat_paths = 0
    #cheat_cnts_by_savings = {}
    for i, loc in enumerate(path):
        #print("Evaluating cheats from path index: " + str(i+1) + " of " + str(len(solution.path)))
        visited.add(loc)
        cheats = race.cheat_moves(loc, cheat_steps)
        for cheat in cheats:
            move, cost = cheat[0], cheat[1]
            if move in visited:
                continue
            ci = path.index(move, i+1)
            save = ci - i - cost
            #print("F: " + str(loc) + ", T: " + str(solution.path[ci]) + ", S: " + str(save))
            if save >= min_save:
                #cheat_cnts_by_savings[save] = cheat_cnts_by_savings.get(save,0) + 1
                cheat_paths += 1
    #print(cheat_cnts_by_savings)
    return cheat_paths

move_adjusts = [(1,0), (-1,0), (0,1), (0,-1)]

class Race:
    """Memory definition"""
    def __init__(self, grid: list[str]) -> None:
        self.height = len(grid)
        self.width = len(grid[0])
        self.start = (0,0)
        self.goal = (0,0)
        self.walls = set()
        for y, row in enumerate(grid):
            for x, col in enumerate(row):
                if col == '#':
                    self.walls.add((x, y))
                elif col == 'S':
                    self.start = (x, y)
                elif col == 'E':
                    self.goal = (x, y)

    def path(self) -> list[tuple[int,int]]:
        """determine the path of the race"""
        path = [self.start]
        loc = self.start
        prev = None
        while loc != self.goal:
            for move in move_adjusts:
                p = (loc[0] + move[0], loc[1] + move[1])
                if p in self.walls or p == prev:
                    continue
                path.append(p)
                prev = loc
                loc = p
                break
        return path

    @functools.cache
    def cheat_moves(self, c: tuple[int,int], steps: int) -> set[tuple[tuple[int,int],int]]:
        """determine potential cheat moves from current location in recursive fashion"""
        locs = set()
        costs = {}
        for move in move_adjusts:
            p = (c[0] + move[0], c[1] + move[1])
            if p[0] < 0 or p[0] >= self.width or p[1] < 0 or p[1] >= self.height:
                continue
            if p not in self.walls:
                locs.add(p)
                costs[p] = 1
            if steps > 1:
                addlt_moves = self.cheat_moves(p, steps-1)
                for m in addlt_moves:
                    mp = m[0]
                    mc = m[1] + 1
                    locs.add(mp)
                    cc = costs.get(mp,-1)
                    if cc == -1 or mc < cc:
                        costs[mp] = mc
        possible = set()
        for l in locs:
            possible.add((l, costs.get(l)))
        return possible

# Data
data = read_lines("input/day20/input.txt")
sample = """###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############""".splitlines()

# Part 1
assert solve_part1(sample, 2) == 44
assert solve_part1(data, 100) == 1441

# Part 2
assert solve_part2(sample, 50) == 285
assert solve_part2(data, 100) == 1021490
