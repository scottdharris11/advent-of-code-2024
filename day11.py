"""utility imports"""
from utilities.data import read_lines
from utilities.runner import runner

@runner("Day 11", "Part 1")
def solve_part1(stones: list[str], blinks: int):
    """part 1 solving function"""
    for _ in range(blinks):
        nstones = list()
        for stone in stones:
            if stone == "0":
                nstones.append("1")
            elif len(stone) % 2 == 0:
                sidx = int(len(stone) / 2)
                nstones.append(stone[:sidx])
                nstones.append(str(int(stone[sidx:])))
            else:
                nstones.append(str(int(stone)*2024))
        stones = nstones
    return len(stones)

@runner("Day 11", "Part 2")
def solve_part2(lines: list[str]):
    """part 2 solving function"""
    return 0

# Data
data = read_lines("input/day11/input.txt")[0].split(" ")
sample = """125 17""".splitlines()[0].split(" ")

# Part 1
assert solve_part1(sample, 6) == 22
assert solve_part1(sample, 25) == 55312
assert solve_part1(data, 25) == 220999

# Part 2
assert solve_part2(sample) == 0
assert solve_part2(data) == 0
