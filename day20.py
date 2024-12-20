"""utility imports"""
from utilities.data import read_lines
from utilities.runner import runner
from utilities.search import Search, Searcher, SearchMove

@runner("Day 20", "Part 1")
def solve_part1(lines: list[str], min_save: int) -> int:
    """part 1 solving function"""
    race = Race(lines)
    ps = PathSearcher(race)
    s = Search(ps)
    solution = s.best(SearchMove(0, race.start))
    if solution is None:
        return -1
    visited = set()
    cheat_paths = 0
    for i, loc in enumerate(solution.path):
        cheats = race.cheat_moves_from(loc, visited)
        for cheat in cheats:
            ci = solution.path.index(cheat, i+1)
            save = ci - i - 2
            #print("F: " + str(loc) + ", T: " + str(solution.path[ci]) + ", S: " + str(save))
            if save >= min_save:
                cheat_paths += 1
        visited.add(loc)
    return cheat_paths

@runner("Day 20", "Part 2")
def solve_part2(lines: list[str]) -> int:
    """part 2 solving function"""
    return 0

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

    def cheat_moves_from(self, c: tuple[int,int], v: set[tuple[int,int]]) -> list[tuple[int,int]]:
        """determine cheat points from current location"""
        possible = []
        for move in move_adusts:
            p = (c[0] + move[0], c[1] + move[1])
            if p not in self.walls:
                continue
            p = (p[0] + move[0], p[1] + move[1])
            if p in self.walls:
                continue
            if p[0] < 0 or p[0] >= self.width or p[1] < 0 or p[1] >= self.height:
                continue
            if p in v:
                continue
            possible.append(p)
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
assert solve_part2(sample) == 0
assert solve_part2(data) == 0
