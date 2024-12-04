"""utility imports"""
from utilities.data import read_lines
from utilities.runner import runner

offsets = [
    (1,0),
    (-1,0),
    (0,1),
    (0,-1),
    (1,1),
    (1,-1),
    (-1,1),
    (-1,-1),
]

@runner("Day 4", "Part 1")
def solve_part1(lines: list):
    """part 1 solving function"""
    height = len(lines)
    width = len(lines[0])
    words = 0
    for y in range(height):
        for x in range(width):
            for offset in offsets:
                if check_word(lines, (x, y), offset):
                    words += 1
    return words

@runner("Day 4", "Part 2")
def solve_part2(lines: list):
    """part 2 solving function"""
    return 0

def check_word(lines: list, loc: tuple, offset: tuple) -> bool:
    """check to see if XMAS is found at the current location and direction"""
    x, y = map(int, loc)
    if lines[y][x] != 'X':
        return False
    height = len(lines)
    width = len(lines[0])
    for letter in ['M', 'A', 'S']:
        x += offset[0]
        if x < 0 or x >= width:
            return False
        y += offset[1]
        if y < 0 or y >= height:
            return False
        if lines[y][x] != letter:
            return False
    return True

# Data
data = read_lines("input/day04/input.txt")
sample = [
    "MMMSXXMASM",
    "MSAMXMSMSA",
    "AMXSXMAAMM",
    "MSAMASMSMX",
    "XMASAMXAMM",
    "XXAMMXXAMA",
    "SMSMSASXSS",
    "SAXAMASAAA",
    "MAMMMXMMMM",
    "MXMXAXMASX"
]

# Part 1
assert solve_part1(sample) == 18
assert solve_part1(data) == 0

# Part 2
assert solve_part2(sample) == 0
assert solve_part2(data) == 0
