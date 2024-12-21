"""utility imports"""
from utilities.data import read_lines
from utilities.runner import runner

@runner("Day 21", "Part 1")
def solve_part1(lines: list[str]) -> int:
    """part 1 solving function"""
    return 0

@runner("Day 21", "Part 2")
def solve_part2(lines: list[str]) -> int:
    """part 2 solving function"""
    return 0

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

    def sequence_paths(self, keyseq: str) -> list[list[chr]]:
        """determine a move path to press the supplied sequence"""
        paths = [""]
        loc = self.a_key
        for key in keyseq:
            kloc = self.key_loc(key)
            kpaths = self.key_paths(loc, kloc)
            wpaths = []
            if kpaths is None:
                for path in paths:
                    wpaths.append(path + "A")
            else:
                for kpath in kpaths:
                    for path in paths:
                        wpaths.append(path + kpath + "A")
            paths = wpaths
            loc = kloc
        return paths

    def key_paths(self, cur: tuple[int,int], goal: tuple[int,int]) -> list[list[chr]]:
        """determine set of path moves that will get from current location to goal"""
        if cur == goal:
            return None
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

    def distance(self, loc1: tuple[int,int], loc2: tuple[int,int]) -> int:
        """compute distance between two locations"""
        return abs(loc1[0]-loc2[0]) + abs(loc1[1]-loc2[1])

    def key_loc(self, key: chr) -> tuple[int,int]:
        """get location for supplied key"""
        for y, row in enumerate(self.layout):
            for x, col in enumerate(row):
                if col == key:
                    return (x,y)
        return None

# Numeric Path Tests
kp = KeyPad(NUMERIC_LAYOUT)
assert kp.a_key == (2,3)
assert kp.key_loc('0') == (1,3)
assert kp.key_paths(kp.a_key, kp.key_loc('0')) == ["<"]
assert kp.key_paths(kp.key_loc('0'), kp.key_loc('2')) == ["^"]
assert len(kp.key_paths(kp.key_loc('2'), kp.key_loc('9'))) == 3
assert ">^^" in kp.key_paths(kp.key_loc('2'), kp.key_loc('9'))
assert "^>^" in kp.key_paths(kp.key_loc('2'), kp.key_loc('9'))
assert "^^>" in kp.key_paths(kp.key_loc('2'), kp.key_loc('9'))
assert len(kp.sequence_paths("029A")) == 3
assert "<A^A>^^AvvvA" in kp.sequence_paths("029A")
assert "<A^A^>^AvvvA" in kp.sequence_paths("029A")
assert "<A^A^^>AvvvA" in kp.sequence_paths("029A")

# Data
data = read_lines("input/day21/input.txt")
sample = """029A
980A
179A
456A
379A""".splitlines()

# Part 1
assert solve_part1(sample) == 0
assert solve_part1(data) == 0

# Part 2
assert solve_part2(sample) == 0
assert solve_part2(data) == 0
