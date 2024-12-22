"""utility imports"""
from utilities.data import read_lines
from utilities.runner import runner

@runner("Day 22", "Part 1")
def solve_part1(lines: list[str]) -> int:
    """part 1 solving function"""
    total = 0
    for line in lines:
        sn = int(line)
        for _ in range(2000):
            sn = secret_number(sn)
        total += sn
    return total

@runner("Day 22", "Part 2")
def solve_part2(lines: list[str]) -> int:
    """part 2 solving function"""
    return 0

def secret_number(sn: int) -> int:
    """calculate next secret number"""
    sn = prune(mix(sn, sn * 64))
    sn = prune(mix(sn, int(sn/32)))
    sn = prune(mix(sn, sn * 2048))
    return sn

def mix(sn: int, val: int) -> int:
    """mix value into secret number"""
    return sn ^ val

def prune(sn: int) -> int:
    """prune secret number values"""
    return sn % 16777216

# Data
data = read_lines("input/day22/input.txt")
sample = """1
10
100
2024""".splitlines()

assert prune(100000000) == 16113920
assert mix(42, 15) == 37
assert secret_number(123) == 15887950
assert secret_number(15887950) == 16495136
assert secret_number(16495136) == 527345
assert secret_number(527345) == 704524
assert secret_number(704524) == 1553684
assert secret_number(1553684) == 12683156
assert secret_number(12683156) == 11100544
assert secret_number(11100544) == 12249484
assert secret_number(12249484) == 7753432
assert secret_number(7753432) == 5908254

# Part 1
assert solve_part1(sample) == 37327623
assert solve_part1(data) == 20332089158

# Part 2
assert solve_part2(sample) == 0
assert solve_part2(data) == 0
