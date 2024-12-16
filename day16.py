"""utility imports"""
from utilities.data import read_lines
from utilities.runner import runner
from utilities.search import PriorityQueue, Search, Searcher, SearchMove

@runner("Day 16", "Part 1")
def solve_part1(lines: list[str]):
    """part 1 solving function"""
    maze = Maze(lines)
    ps = PathSearcher(maze)
    s = Search(ps)
    solution = s.best(SearchMove(0, maze.start))
    if solution is None:
        return -1
    return solution.cost

@runner("Day 16", "Part 2")
def solve_part2(lines: list[str]):
    """part 2 solving function"""
    maze = Maze(lines)

    # start with the best path
    ps = PathSearcher(maze)
    s = Search(ps)
    solution = s.best(SearchMove(0, maze.start))
    if solution is None:
        return -1

    # look for alternative paths by putting a wall at the turn points
    # of the path, and searching for new paths that match the cost
    alt_runs = PriorityQueue()
    best_path_cost = solution.cost
    best_locs = set()
    workd = solution.path[0].direction
    for pe in solution.path:
        best_locs.add(pe.loc)
        if pe.direction != workd:
            adjust = move_adusts[pe.direction]
            wpoint = (pe.loc[0] + adjust[0], pe.loc[1] + adjust[1])
            walls = set()
            walls.add(wpoint)
            alt_runs.queue(frozenset(walls), 1)
            workd = pe.direction
    alts_checked = set()
    skip = set()
    while not alt_runs.empty():
        walls = alt_runs.next()
        if walls in alts_checked:
            continue
        alts_checked.add(walls)
        find_alt_path(maze, best_path_cost, alt_runs, best_locs, walls, skip)
    return len(best_locs)

EAST = 'E'
WEST = 'W'
NORTH = 'N'
SOUTH = 'S'
rotations = {EAST: [SOUTH, NORTH], WEST: [SOUTH, NORTH], SOUTH: [EAST, WEST], NORTH: [EAST, WEST]}
move_adusts = {EAST: (1,0), WEST: (-1,0), SOUTH: (0,1), NORTH:(0,-1)}

class LocDir:
    """represent the current location and direction"""
    def __init__(self, loc: tuple[int], d: chr) -> None:
        self.loc = loc
        self.direction = d

    def __repr__(self):
        return str((self.loc, self.direction))

    def __hash__(self) -> int:
        return hash((self.loc[0], self.loc[1], self.direction))

    def __eq__(self, other: object) -> bool:
        if other is None:
            return False
        if self.loc != other.loc:
            return False
        if self.direction != other.direction:
            return False
        return True

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

class Maze:
    """Maze definition"""
    def __init__(self, lines: list[str]) -> None:
        self.grid = lines
        for y, row in enumerate(self.grid):
            for x, col in enumerate(row):
                if col == "S":
                    self.start = LocDir((x, y), EAST)
                elif col == "E":
                    self.goal = (x, y)
        self.addlt_walls = set()

    def is_goal(self, point: tuple[int]) -> bool:
        """determine if the supplied point is the goal"""
        return point == self.goal

    def moves_from(self, current: LocDir) -> list[tuple[LocDir,int]]:
        """determine possible moves from curent location"""
        possible = []
        adjust = move_adusts[current.direction]
        npoint = (current.loc[0] + adjust[0], current.loc[1] + adjust[1])
        if not self.grid[npoint[1]][npoint[0]] == "#" and npoint not in self.addlt_walls:
            possible.append((LocDir(npoint,current.direction),1))
        for rotate in rotations[current.direction]:
            radjust = move_adusts[rotate]
            rpoint = (current.loc[0] + radjust[0], current.loc[1] + radjust[1])
            if not self.grid[rpoint[1]][rpoint[0]] == "#":
                possible.append((LocDir(current.loc, rotate),1000))
        return possible

    def distance_from_goal(self, current: LocDir) -> int:
        """calculate distance from the goal"""
        d = 0
        if current.loc[0] < self.goal[0] and current.direction != EAST:
            d += 1000
        if current.loc[0] > self.goal[0] and current.direction != WEST:
            d += 1000
        if current.loc[1] < self.goal[1] and current.direction != SOUTH:
            d += 1000
        if current.loc[1] > self.goal[1] and current.direction != NORTH:
            d += 1000
        d += (abs(current.loc[0] - self.goal[0]) + abs(current.loc[1] - self.goal[1]))
        return d

class PathSearcher(Searcher):
    """path search implementation for the maze"""
    def __init__(self, maze: Maze) -> None:
        self.maze = maze

    def is_goal(self, obj: LocDir) -> bool:
        """determine if search has reached its goal"""
        return self.maze.is_goal(obj.loc)

    def possible_moves(self, obj: LocDir) -> list[SearchMove]:
        """determine possible moves from current location"""
        possible = []
        for move in self.maze.moves_from(obj):
            possible.append(SearchMove(move[1], move[0]))
        return possible

    def distance_from_goal(self, obj: LocDir) -> int:
        """determine distance from goal"""
        return self.maze.distance_from_goal(obj)

def find_alt_path(maze: Maze, cost: int, pq: PriorityQueue, best: set, walls: set[tuple[int,int]], skip: set):
    """attempt to find alternate paths by placing additional walls"""
    maze.addlt_walls = walls
    ps = PathSearcher(maze)
    s = Search(ps)
    solution = s.best(SearchMove(0, maze.start))
    if solution is None or solution.cost != cost:
        for w in walls:
            skip.add(w)
        return
    workd = solution.path[0].direction
    for pe in solution.path:
        best.add(pe.loc)
        if pe.direction != workd:
            adjust = move_adusts[pe.direction]
            workd = pe.direction
            wpoint = (pe.loc[0] + adjust[0], pe.loc[1] + adjust[1])
            if wpoint in skip:
                continue
            nwalls = set()
            for w in walls:
                nwalls.add(w)
            nwalls.add(wpoint)
            pq.queue(frozenset(nwalls), 1)
    return

# Data
data = read_lines("input/day16/input.txt")
sample = """###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############""".splitlines()
sample2 = """#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################""".splitlines()

# Part 1
assert solve_part1(sample) == 7036
assert solve_part1(sample2) == 11048
assert solve_part1(data) == 90440

# Part 2
assert solve_part2(sample) == 45
assert solve_part2(sample2) == 64
assert solve_part2(data) == 479
