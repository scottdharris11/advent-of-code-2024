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
    return complexity_total(lines, 4)

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

    def best_press_paths(self, keyseq: str, current: tuple[int,int]) -> list[str]:
        """determine the best path to press the supplied key sequence from the supplied location"""
        print("calculating path for sequence length: " + str(len((keyseq))))
        kloc = self.key_loc(keyseq[0])
        if kloc == current:
            kpaths = [""]
        else:
            kpaths = self.key_paths(current, kloc)

        paths = []
        if len(keyseq) == 1:
            for p in kpaths:
                paths.append(p + "A")
        else:
            addlt = self.best_press_paths(keyseq[1:], kloc)
            for a in addlt:
                for k in kpaths:
                    paths.append(k + "A" + a)

        print("potential paths discovered: " + str(len(paths)))
        if len(paths) == 1:
            return paths

        min_score = -1
        paths_by_score = {}
        for path in paths:
            score = self.score_seq(path)
            if min_score == -1 or score <= min_score:
                min_score = score
                pbs = paths_by_score.get(score, [])
                pbs.append(path)
                paths_by_score[score] = pbs
        return paths_by_score[min_score]

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

    def score_seq(self, keyseq: str) -> int:
        """score a sequence based on movements required from each back to a-key"""
        score = 0
        for k in keyseq:
            kloc = self.key_loc(k)
            if kloc is None:
                continue
            score += self.distance(kloc, self.a_key) * 2
        return score

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
    keypads = []
    for _ in range(robot_cnt):
        keypads.append(dkp)
    keypads.append(nkp)

    total = 0
    for code in codes:
        total += code_complexity(code, keypads)
    return total

def code_complexity(code: str, keypads: list[KeyPad]) -> int:
    """compute the code complexity for a code"""
    print("processing code: " + code)
    path = ""
    npk = keypads[-1]
    loc = npk.a_key
    for k in code:
        print("looking for path for code: " + k)
        paths = button_path([k], keypads, loc)
        path += paths[0]
        loc = npk.key_loc(k)
    #print(code + ": " + path)
    return int(code[:-1]) * len(path)

def button_path(key_seqs: list[str], keypads: list[KeyPad], start: tuple[int,int]) -> list[str]:
    """build best set of paths to achieve supplied key_seqs on supplied keypads"""
    print("button path sequences: " + str(len(key_seqs)) + ", keypad: " + str(len(keypads)))
    kp = keypads[-1]
    paths_by_score = {}
    min_score = -1
    seq = 1
    for key_seq in key_seqs:
        print("sequence: " + str(seq))
        seq += 1
        bpaths = kp.best_press_paths(key_seq, start)
        for p in bpaths:
            score = kp.score_seq(p)
            if min_score == -1 or score <= min_score:
                min_score = score
                pbs = paths_by_score.get(score, [])
                pbs.append(p)
                paths_by_score[score] = pbs
    bpaths = paths_by_score[min_score]
    if len(keypads) == 1:
        return bpaths
    return button_path(bpaths, keypads[:-1], keypads[-2].a_key)

# KeyPad Tests
nkp = KeyPad(NUMERIC_LAYOUT)
dkp = KeyPad(DIRECTIONAL_LAYOUT)

assert nkp.a_key == (2,3)
assert nkp.key_loc('0') == (1,3)
assert nkp.key_paths(nkp.a_key, nkp.key_loc('0')) == ["<"]
assert nkp.key_paths(nkp.key_loc('0'), nkp.key_loc('2')) == ["^"]
assert len(nkp.key_paths(nkp.key_loc('2'), nkp.key_loc('9'))) == 3
assert ">^^" in nkp.key_paths(nkp.key_loc('2'), nkp.key_loc('9'))
assert "^>^" in nkp.key_paths(nkp.key_loc('2'), nkp.key_loc('9'))
assert "^^>" in nkp.key_paths(nkp.key_loc('2'), nkp.key_loc('9'))
#assert len(nkp.best_press_paths("029A", nkp.a_key)) == 3
#assert "<A^A>^^AvvvA" in nkp.best_press_paths("029A", nkp.a_key)
#assert "<A^A^>^AvvvA" in nkp.best_press_paths("029A", nkp.a_key)
#assert "<A^A^^>AvvvA" in nkp.best_press_paths("029A", nkp.a_key)

#assert dkp.a_key == (2,0)
#assert "v<<A>>^A<A>AvA<^AA>A<vAAA>^A" in dkp.best_press_paths("<A^A>^^AvvvA", dkp.a_key)
#assert "<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A" in dkp.best_press_paths("v<<A>>^A<A>AvA<^AA>A<vAAA>^A", dkp.a_key)

# Data
data = read_lines("input/day21/input.txt")
sample = """029A
980A
179A
456A
379A""".splitlines()

# Part 1
#assert solve_part1(sample) == 126384
#assert solve_part1(data) == 212488

# Part 2
assert solve_part2(data) == 0
