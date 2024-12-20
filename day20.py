"""utility imports"""
import functools
from utilities.data import read_lines
from utilities.runner import runner
from utilities.search import Search, Searcher, SearchMove

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
    s = Search(PathSearcher(race))
    solution = s.best(SearchMove(0, race.start))
    if solution is None:
        return -1
    visited = set()
    cheat_paths = 0
    #cheat_cnts_by_savings = {}
    for i, loc in enumerate(solution.path):
        #print("Evaluating cheats from path index: " + str(i+1) + " of " + str(len(solution.path)))
        visited.add(loc)
        cheats = race.cheat_moves(loc, cheat_steps)
        for cheat in cheats:
            move, cost = cheat[0], cheat[1]
            if move in visited:
                continue
            ci = solution.path.index(move, i+1)
            save = ci - i - cost
            #print("F: " + str(loc) + ", T: " + str(solution.path[ci]) + ", S: " + str(save))
            if save >= min_save:
                #cheat_cnts_by_savings[save] = cheat_cnts_by_savings.get(save,0) + 1
                cheat_paths += 1
    #print(cheat_cnts_by_savings)
    return cheat_paths

move_adusts = [(1,0), (-1,0), (0,1), (0,-1)]

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

    def is_goal(self, point: tuple[int, int]) -> bool:
        """determine if the supplied point is the goal"""
        return point == self.goal

    @functools.cache
    def cheat_moves(self, c: tuple[int,int], steps: int) -> set[tuple[tuple[int,int],int]]:
        """determine potential cheat moves from current location in recursive fashion"""
        locs = set()
        costs = {}
        for move in move_adusts:
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

    def moves_from(self, current: tuple[int,int]) -> list[tuple[int,int]]:
        """determine possible moves from curent location"""
        possible = []
        for move in move_adusts:
            point = (current[0] + move[0], current[1] + move[1])
            if point[0] < 0 or point[0] >= self.width or point[1] < 0 or point[1] >= self.height:
                continue
            if point in self.walls:
                continue
            possible.append(point)
        return possible

    def distance_from_goal(self, current: tuple[int,int]) -> int:
        """calculate distance from the goal"""
        return (abs(current[0] - self.goal[0]) + abs(current[1] - self.goal[1]))

class PathSearcher(Searcher):
    """path search implementation for the memory"""
    def __init__(self, race: Race) -> None:
        self.race = race

    def is_goal(self, obj: tuple[int,int]) -> bool:
        """determine if search has reached its goal"""
        return self.race.is_goal(obj)

    def possible_moves(self, obj: tuple[int,int]) -> list[SearchMove]:
        """determine possible moves from current location"""
        possible = []
        for move in self.race.moves_from(obj):
            possible.append(SearchMove(1, move))
        return possible

    def distance_from_goal(self, obj: tuple[int,int]) -> int:
        """determine distance from goal"""
        return self.race.distance_from_goal(obj)

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
