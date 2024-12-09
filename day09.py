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
    diskmap = DiskMap(lines[0])
    diskmap.defrag()
    return diskmap.checksum()

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
    def __init__(self, s: str) -> None:
        self.entries = []
        file = True
        file_no = 0
        for c in s:
            blocks = int(c)
            if file:
                self.entries.append(File(file_no, blocks))
                file_no += 1
            else:
                self.entries.append(FreeSpace(blocks))
            file = not file

    def __repr__(self):
        return ''.join(map(str,self.entries))

    def last_file_idx(self) -> int:
        """obtain index to last file"""
        for i in range(len(self.entries)-1, 0, -1):
            if isinstance(self.entries[i], File):
                return i
        return -1

    def index_of_file(self, file_id: int) -> int:
        """obtain index to last file"""
        for i in range(len(self.entries)-1, 0, -1):
            if isinstance(self.entries[i], File) and self.entries[i].file_id == file_id:
                return i
        return -1

    def first_free_idx(self) -> int:
        """obtain index to first free space"""
        for i, e in enumerate(self.entries):
            if isinstance(e, FreeSpace):
                return i
        return -1

    def compress(self):
        """compress files into leftmost free space"""
        file_idx = self.last_file_idx()
        free_idx = self.first_free_idx()
        while file_idx >= 0 and free_idx >= 0 and file_idx > free_idx:
            file = self.entries[file_idx]
            free = self.entries[free_idx]
            if file.blocks == free.blocks:
                self.entries[free_idx] = file
                self.entries[file_idx] = free
            elif file.blocks < free.blocks:
                self.entries.insert(free_idx, file)
                if file_idx + 2 < len(self.entries) and isinstance(self.entries[file_idx+2], FreeSpace):
                    self.entries[file_idx+2].blocks += file.blocks
                    del self.entries[file_idx+1]
                else:
                    self.entries[file_idx+1] = FreeSpace(file.blocks)
                free.blocks -= file.blocks
            else:
                self.entries[free_idx] = File(file.file_id, free.blocks)
                file.blocks -= free.blocks
                if file_idx + 1 < len(self.entries) and isinstance(self.entries[file_idx+1], FreeSpace):
                    self.entries[file_idx+1].blocks += free.blocks
                else:
                    self.entries.insert(file_idx+1,FreeSpace(free.blocks))
            file_idx = self.last_file_idx()
            free_idx = self.first_free_idx()

    def defrag(self):
        """compress free space by moving complete files left"""
        last_file = self.entries[self.last_file_idx()]
        for file_id in range(last_file.file_id, -1, -1):
            file_idx = self.index_of_file(file_id)
            file = self.entries[file_idx]
            free_idx = self.first_free_idx()
            while free_idx < file_idx:
                free = self.entries[free_idx]
                if file.blocks == free.blocks:
                    self.entries[free_idx] = file
                    self.entries[file_idx] = free
                    break
                elif file.blocks < free.blocks:
                    self.entries.insert(free_idx, file)
                    if file_idx + 2 < len(self.entries) and isinstance(self.entries[file_idx+2], FreeSpace):
                        self.entries[file_idx+2].blocks += file.blocks
                        del self.entries[file_idx+1]
                    else:
                        self.entries[file_idx+1] = FreeSpace(file.blocks)
                    free.blocks -= file.blocks
                    break
                free_idx += 1
                while free_idx < len(self.entries):
                    if isinstance(self.entries[free_idx], FreeSpace):
                        break
                    free_idx += 1

    def checksum(self) -> int:
        """compute checksum for diskmap"""
        chk = 0
        idx = 0
        for e in self.entries:
            if isinstance(e, FreeSpace):
                idx += e.blocks
                continue
            for _ in range(e.blocks):
                chk += e.file_id * idx
                idx += 1
        return chk

# Data
data = read_lines("input/day09/input.txt")
sample = """2333133121414131402""".splitlines()

# Part 1
assert solve_part1(sample) == 1928
assert solve_part1(data) == 6607511583593

# Part 2
assert solve_part2(sample) == 2858
assert solve_part2(data) == 6636608781232
