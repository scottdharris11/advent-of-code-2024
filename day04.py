"""utility imports"""
from utilities.data import read_lines
from utilities.runner import runner

xmas_offsets = [
    (1,0),
    (-1,0),
    (0,1),
    (0,-1),
    (1,1),
    (1,-1),
    (-1,1),
    (-1,-1),
]

x_mas_offsets = [
    [(-1,-1),(1,1)],
    [(-1,1),(1,-1)]
]

@runner("Day 4", "Part 1")
def solve_part1(lines: list):
    """part 1 solving function"""
    height = len(lines)
    width = len(lines[0])
    words = 0
    for y in range(height):
        for x in range(width):
            for offset in xmas_offsets:
                if check_xmas(lines, (x, y), offset):
                    words += 1
    return words

@runner("Day 4", "Part 2")
def solve_part2(lines: list):
    """part 2 solving function"""
    height = len(lines)
    width = len(lines[0])
    words = 0
    for y in range(height):
        for x in range(width):
            if check_x_mas(lines, (x, y)):
                words += 1
    return words

def check_xmas(lines: list, loc: tuple, offset: tuple) -> bool:
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

def check_x_mas(lines: list, loc: tuple) -> bool:
    """check to see if X-MAS is formed at the current location"""
    x, y = map(int, loc)
    if lines[y][x] != 'A':
        return False
    height = len(lines)
    width = len(lines[0])

    for offsets in x_mas_offsets:
        x1 = x + offsets[0][0]
        x2 = x + offsets[1][0]
        if x1 < 0 or x1 >= width or x2 < 0 or x2 >= width:
            return False
        y1 = y + offsets[0][1]
        y2 = y + offsets[1][1]
        if y1 < 0 or y1 >= height or y2 < 0 or y2 >= height:
            return False
        if lines[y1][x1] == 'M':
            if lines[y2][x2] != 'S':
                return False
        elif lines[y1][x1] == 'S':
            if lines[y2][x2] != 'M':
                return False
        else:
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
assert solve_part1(data) == 2578

# Part 2
assert solve_part2(sample) == 9
assert solve_part2(data) == 1972
