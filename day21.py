"""utility imports"""
import functools
from utilities.data import read_lines
from utilities.runner import runner

@runner("Day 21", "Part 1")
def solve_part1(lines: list[str]) -> int:
    """part 1 solving function"""
    return complexity_total(lines, 2)

@runner("Day 21", "Part 2")
def solve_part2(lines: list[str]) -> int:
    """part 2 solving function"""
    return complexity_total(lines, 25)

MOVES = {(0,-1): '^', (0,1): 'v', (-1,0): '<', (1,0): '>'}
NUMERIC_LAYOUT = [['7', '8', '9'],['4', '5', '6'],['1', '2', '3'],[None, '0', 'A']]
DIRECTIONAL_LAYOUT = [[None, '^', 'A'], ['<', 'v', '>']]

class KeyPad:
    """Keypad implementation"""
    def __init__(self, layout: list[str]):
        self.layout = layout
        self.height = len(self.layout)
        self.width = len(self.layout[0])
        for y, row in enumerate(self.layout):
            for x, col in enumerate(row):
                if col is None:
                    self.blank = (x,y)
                elif col == 'A':
                    self.a_key = (x,y)

    @functools.cache
    def path_len(self, cur: tuple[int,int], goal: tuple[int,int], depth: int) -> int:
        """determine the length of the optimal path for a key at certain depth"""
        paths = self.key_paths(cur, goal)
        if depth == 1:
            return len(paths[0])
        min_len = -1
        for path in paths:
            l = 0
            c = self.a_key
            for k in path:
                k_loc = self.key_loc(k)
                l += self.path_len(c, k_loc, depth - 1)
                c = k_loc
            if min_len == -1 or l < min_len:
                min_len = 1
        return min_len

    @functools.cache
    def key_paths(self, cur: tuple[int,int], goal: tuple[int,int]) -> list[str]:
        """determine set of path moves that will get from current location to goal"""
        if cur == goal:
            return ["A"]
        cdist = self.distance(cur, goal)
        paths = []
        for move in [(0,-1), (0,1), (-1,0), (1,0)]:
            loc = (cur[0]+move[0], cur[1]+move[1])
            if loc[0] < 0 or loc[0] >= self.width or loc[1] < 0 or loc[1] >= self.height:
                continue
            if self.layout[loc[1]][loc[0]] is None:
                continue
            ldist = self.distance(loc, goal)
            if ldist >= cdist:
                continue
            addlt = self.key_paths(loc, goal)
            if addlt is None:
                paths.append(MOVES[move])
            else:
                for a in addlt:
                    paths.append(MOVES[move] + a)
        return paths

    @functools.cache
    def distance(self, loc1: tuple[int,int], loc2: tuple[int,int]) -> int:
        """compute distance between two locations"""
        return abs(loc1[0]-loc2[0]) + abs(loc1[1]-loc2[1])

    @functools.cache
    def key_loc(self, key: chr) -> tuple[int,int]:
        """get location for supplied key"""
        for y, row in enumerate(self.layout):
            for x, col in enumerate(row):
                if col == key:
                    return (x,y)
        return None

def complexity_total(codes: list[str], robot_cnt: int) -> int:
    """compute the complexity total for the supplied codes and keypad sequences"""
    total = 0
    for code in codes:
        total += code_complexity(code, robot_cnt)
    return total

def code_complexity(code: str, robot_cnt: int) -> int:
    """compute the code complexity for a code"""
    print("processing code: " + code)
    numeric = KeyPad(NUMERIC_LAYOUT)
    directional = KeyPad(DIRECTIONAL_LAYOUT)
    np_loc = numeric.a_key
    path_len = 0
    for k in code:
        k_loc = numeric.key_loc(k)
        number_paths = numeric.key_paths(np_loc, k_loc)
        np_loc = k_loc
        best = -1
        for dp in number_paths:
            print(dp)
            pl = 0
            for dpk in dp:
                dpk_loc = directional.key_loc(dpk)
                pl += directional.path_len(directional.a_key, dpk_loc, robot_cnt)
            if best == -1 or pl < best:
                best = pl
        path_len += best
    return int(code[:-1]) * path_len

# KeyPad Tests
nkp = KeyPad(NUMERIC_LAYOUT)
dkp = KeyPad(DIRECTIONAL_LAYOUT)

assert nkp.a_key == (2,3)
assert nkp.key_loc('0') == (1,3)
assert nkp.key_paths(nkp.a_key, nkp.key_loc('0')) == ["<A"]
assert nkp.key_paths(nkp.key_loc('0'), nkp.key_loc('2')) == ["^A"]
assert len(nkp.key_paths(nkp.key_loc('2'), nkp.key_loc('9'))) == 3
assert ">^^A" in nkp.key_paths(nkp.key_loc('2'), nkp.key_loc('9'))
assert "^>^A" in nkp.key_paths(nkp.key_loc('2'), nkp.key_loc('9'))
assert "^^>A" in nkp.key_paths(nkp.key_loc('2'), nkp.key_loc('9'))

# Data
data = read_lines("input/day21/input.txt")
sample = """029A
980A
179A
456A
379A""".splitlines()

# Part 1
assert solve_part1(sample) == 126384
#assert solve_part1(data) == 212488

# Part 2
#assert solve_part2(data) == 0
