"""utility imports"""
from utilities.data import read_lines, parse_integers
from utilities.runner import runner
from utilities.search import Search, Searcher, SearchMove

@runner("Day 18", "Part 1")
def solve_part1(coords: list[str], size: int, byte_count: int):
    """part 1 solving function"""
    maze = Memory(coords, size, byte_count)
    ps = PathSearcher(maze)
    s = Search(ps)
    solution = s.best(SearchMove(0, (0,0)))
    if solution is None:
        return -1
    return solution.cost

@runner("Day 18", "Part 2")
def solve_part2(lines: list[str]):
    """part 2 solving function"""
    return 0

move_adusts = [(1,0), (-1,0), (0,1), (0,-1)]

class Memory:
    """Memory definition"""
    def __init__(self, coords: list[str], size: int, byte_count: int) -> None:
        self.size = size
        self.goal = (self.size-1, self.size-1)
        self.corrupted = set()
        for i in range(byte_count):
            c = parse_integers(coords[i],",")
            self.corrupted.add((c[0], c[1]))

    def is_goal(self, point: tuple[int]) -> bool:
        """determine if the supplied point is the goal"""
        return point == (self.size-1, self.size-1)

    def moves_from(self, current: tuple[int,int]) -> list[tuple[int,int]]:
        """determine possible moves from curent location"""
        possible = []
        for move in move_adusts:
            point = (current[0] + move[0], current[1] + move[1])
            if point[0] < 0 or point[0] >= self.size or point[1] < 0 or point[1] >= self.size:
                continue
            if point in self.corrupted:
                continue
            possible.append(point)
        return possible

    def distance_from_goal(self, current: tuple[int,int]) -> int:
        """calculate distance from the goal"""
        return (abs(current[0] - self.goal[0]) + abs(current[1] - self.goal[1]))

class PathSearcher(Searcher):
    """path search implementation for the memory"""
    def __init__(self, memory: Memory) -> None:
        self.memory = memory

    def is_goal(self, obj: tuple[int,int]) -> bool:
        """determine if search has reached its goal"""
        return self.memory.is_goal(obj)

    def possible_moves(self, obj: tuple[int,int]) -> list[SearchMove]:
        """determine possible moves from current location"""
        possible = []
        for move in self.memory.moves_from(obj):
            possible.append(SearchMove(1, move))
        return possible

    def distance_from_goal(self, obj: tuple[int,int]) -> int:
        """determine distance from goal"""
        return self.memory.distance_from_goal(obj)

# Data
data = read_lines("input/day18/input.txt")
sample = """5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0""".splitlines()

# Part 1
assert solve_part1(sample, 7, 12) == 22
assert solve_part1(data, 71, 1024) == 334

# Part 2
assert solve_part2(sample) == 0
assert solve_part2(data) == 0
