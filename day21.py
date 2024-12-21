"""utility imports"""
import functools
from utilities.data import read_lines
from utilities.runner import runner

@runner("Day 21", "Part 1")
def solve_part1(lines: list[str]) -> int:
    """part 1 solving function"""
    return complexity_total(lines, [dkp, dkp, nkp])

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

    @functools.cache
    def sequence_paths(self, keyseq: str) -> list[str]:
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

    @functools.cache
    def key_paths(self, cur: tuple[int,int], goal: tuple[int,int]) -> list[str]:
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

def complexity_total(codes: list[str], kp_seq: list[KeyPad]) -> int:
    """compute the complexity total for the supplied codes and keypad sequences"""
    total = 0
    for code in codes:
        paths = button_paths(code, kp_seq)
        path = paths[0]
        for i in range(1, len(paths)):
            if len(paths[i]) < len(path):
                path = paths[i]
        #print(code + ": " + path)
        total += int(code[:-1]) * len(path)
    return total

def button_paths(keys: str, keypads: list[KeyPad]) -> list[str]:
    """build set of possible button paths for the keys"""
    kpl = len(keypads)
    kp = keypads[kpl-1]
    paths = []
    for p in kp.sequence_paths(keys):
        if kpl == 1:
            paths.append(p)
        else:
            for kpp in button_paths(p, keypads[:kpl-1]):
                paths.append(kpp)
    return paths

# KeyPad Tests
nkp = KeyPad(NUMERIC_LAYOUT)

assert nkp.a_key == (2,3)
assert nkp.key_loc('0') == (1,3)
assert nkp.key_paths(nkp.a_key, nkp.key_loc('0')) == ["<"]
assert nkp.key_paths(nkp.key_loc('0'), nkp.key_loc('2')) == ["^"]
assert len(nkp.key_paths(nkp.key_loc('2'), nkp.key_loc('9'))) == 3
assert ">^^" in nkp.key_paths(nkp.key_loc('2'), nkp.key_loc('9'))
assert "^>^" in nkp.key_paths(nkp.key_loc('2'), nkp.key_loc('9'))
assert "^^>" in nkp.key_paths(nkp.key_loc('2'), nkp.key_loc('9'))
assert len(nkp.sequence_paths("029A")) == 3
assert "<A^A>^^AvvvA" in nkp.sequence_paths("029A")
assert "<A^A^>^AvvvA" in nkp.sequence_paths("029A")
assert "<A^A^^>AvvvA" in nkp.sequence_paths("029A")

dkp = KeyPad(DIRECTIONAL_LAYOUT)
assert dkp.a_key == (2,0)
assert "v<<A>>^A<A>AvA<^AA>A<vAAA>^A" in dkp.sequence_paths("<A^A>^^AvvvA")
assert "<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A" in dkp.sequence_paths("v<<A>>^A<A>AvA<^AA>A<vAAA>^A")

# Data
data = read_lines("input/day21/input.txt")
sample = """029A
980A
179A
456A
379A""".splitlines()

# Part 1
assert solve_part1(sample) == 126384
assert solve_part1(data) == 212488

# Part 2
assert solve_part2(data) == 0
