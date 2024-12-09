"""utility imports"""
from utilities.data import read_lines
from utilities.runner import runner

@runner("Day 9", "Part 1")
def solve_part1(lines: list[str]):
    """part 1 solving function"""
    diskmap = DiskMap(lines[0])
    diskmap.compress()
    return diskmap.checksum()

@runner("Day 9", "Part 2")
def solve_part2(lines: list[str]):
    """part 2 solving function"""
    return 0

class File:
    """file definition"""
    def __init__(self, file_id: int, blocks: int) -> None:
        self.file_id = file_id
        self.blocks = blocks

    def __repr__(self):
        return str(self.file_id) * self.blocks

class FreeSpace:
    """free space definition"""
    def __init__(self, blocks: int) -> None:
        self.blocks = blocks

    def __repr__(self):
        return "." * self.blocks
    
class DiskMap:
    """diskmap definition"""
    def __init__(self, line: str) -> None:
        self.blocks = ""
        file = True
        file_no = 0
        for c in line:
            blocks = int(c)
            if file:
                self.blocks += str(file_no) * blocks
                file_no += 1
            else:
                self.blocks += "." * blocks
            file = not file

    def __repr__(self):
        return self.blocks

    def compress(self):
        """compress files into leftmost free space"""
        work = list(self.blocks)
        file_idx = len(self.blocks) - 1
        free_idx = 0
        while True:
            while work[free_idx] != '.':
                free_idx += 1
            while work[file_idx] == '.':
                file_idx -= 1
            if file_idx < free_idx:
                break
            work[free_idx] = work[file_idx]
            work[file_idx] = '.'
        self.blocks = "".join(work)

    def checksum(self) -> int:
        """compute checksum for diskmap"""
        chk = 0
        for i, c in enumerate(self.blocks):
            if c != '.':
                chk += int(c) * i
        return chk

# Data
data = read_lines("input/day09/input.txt")
sample = """2333133121414131402""".splitlines()

# Part 1
assert solve_part1(sample) == 1928
assert solve_part1(data) > 93714629328

# Part 2
assert solve_part2(sample) == 0
assert solve_part2(data) == 0
