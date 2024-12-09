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
        self.etype = "file"
        self.file_id = file_id
        self.blocks = blocks

    def __repr__(self):
        return str(self.file_id) * self.blocks

class FreeSpace:
    """free space definition"""
    def __init__(self, blocks: int) -> None:
        self.etype = "free"
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

    def last_file_idx(self, start=-1) -> int:
        """obtain index to last file"""
        if start < 0 or start >= len(self.entries):
            start = len(self.entries)-1
        for i in range(start, 0, -1):
            if self.entries[i].etype == "file":
                return i
        return -1

    def index_of_file(self, file_id: int, start=-1) -> int:
        """obtain index to last file"""
        if start < 0 or start >= len(self.entries):
            start = len(self.entries)-1
        for i in range(start, 0, -1):
            if self.entries[i].etype == "file" and self.entries[i].file_id == file_id:
                return i
        return -1

    def first_free_idx(self, start=0) -> int:
        """obtain index to first free space"""
        for i in range(start, len(self.entries),1):
            if self.entries[i].etype == "free":
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
                if file_idx + 2 < len(self.entries) and self.entries[file_idx+2].etype == "free":
                    self.entries[file_idx+2].blocks += file.blocks
                    del self.entries[file_idx+1]
                else:
                    self.entries[file_idx+1] = FreeSpace(file.blocks)
                free.blocks -= file.blocks
            else:
                self.entries[free_idx] = File(file.file_id, free.blocks)
                file.blocks -= free.blocks
                if file_idx + 1 < len(self.entries) and self.entries[file_idx+1].etype == "free":
                    self.entries[file_idx+1].blocks += free.blocks
                else:
                    self.entries.insert(file_idx+1,FreeSpace(free.blocks))
            file_idx = self.last_file_idx(file_idx+1)
            free_idx = self.first_free_idx(free_idx)

    def defrag(self):
        """compress free space by moving complete files left"""
        file_idx = self.last_file_idx()
        last_file = self.entries[file_idx]
        entry_count = len(self.entries)
        for file_id in range(last_file.file_id, -1, -1):
            file_idx = self.index_of_file(file_id, file_idx)
            file = self.entries[file_idx]
            free_idx = self.first_free_idx()
            while free_idx < file_idx:
                free = self.entries[free_idx]
                if file.blocks == free.blocks:
                    self.entries[free_idx] = file
                    self.entries[file_idx] = free
                    break
                if file.blocks < free.blocks:
                    self.entries.insert(free_idx, file)
                    entry_count += 1
                    if file_idx + 2 < entry_count and self.entries[file_idx+2].etype == "free":
                        self.entries[file_idx+2].blocks += file.blocks
                        del self.entries[file_idx+1]
                        entry_count -= 1
                    else:
                        self.entries[file_idx+1] = FreeSpace(file.blocks)
                    free.blocks -= file.blocks
                    break
                free_idx += 1
                while free_idx < entry_count:
                    if self.entries[free_idx].etype == "free":
                        break
                    free_idx += 1

    def checksum(self) -> int:
        """compute checksum for diskmap"""
        chk = 0
        idx = 0
        for e in self.entries:
            if e.etype == "free":
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
