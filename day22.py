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
    change_seqs = {}
    for line in lines:
        sn = int(line)
        p = price(sn)
        bcs = set()
        bc = []
        for i in range(2000):
            nsn = secret_number(sn)
            np = price(nsn)
            pc = np-p
            bc.append(pc)
            if i > 2:
                seq = (bc[i-3], bc[i-2], bc[i-1], bc[i])
                if seq not in bcs:
                    bcs.add(seq)
                    change_seqs[seq] = change_seqs.get(seq,0) + np
            sn = nsn
            p = np
    values = list(change_seqs.values())
    values.sort()
    return values[-1]

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

def price(sn: int) -> int:
    """price value of a secret number"""
    return sn % 10

# Data
data = read_lines("input/day22/input.txt")
sample = """1
10
100
2024""".splitlines()
sample2 = """1
2
3
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
assert price(123) == 3
assert price(15887950) == 0
assert price(16495136) == 6
assert price(527345) == 5
assert price(704524) == 4
assert price(1553684) == 4
assert price(12683156) == 6
assert price(11100544) == 4
assert price(12249484) == 4
assert price(7753432) == 2

# Part 1
assert solve_part1(sample) == 37327623
assert solve_part1(data) == 20332089158

# Part 2
assert solve_part2(sample2) == 23
assert solve_part2(data) == 2191
