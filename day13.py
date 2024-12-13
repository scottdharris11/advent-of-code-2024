"""utility imports"""
import re
from utilities.data import read_lines
from utilities.runner import runner

@runner("Day 13", "Part 1")
def solve_part1(lines: list[str]):
    """part 1 solving function"""
    machines = parse_machines(lines)
    tokens = 0
    for m in machines:
        tokens += m.winning_tokens()
    return tokens

@runner("Day 13", "Part 2")
def solve_part2(lines: list[str]):
    """part 2 solving function"""
    adjust = 10000000000000
    machines = parse_machines(lines)
    tokens = 0
    for m in machines:
        m.constraint = 0
        m.prize = (m.prize[0]+adjust, m.prize[1]+adjust)
        tokens += m.winning_tokens()
    return tokens

class PrizeMachine:
    """Claw prize machine"""
    def __init__(self, a_btn: tuple[int,int], b_btn: tuple[int,int], prize: tuple[int,int]) -> None:
        self.a_btn = a_btn
        self.b_btn = b_btn
        self.prize = prize
        self.constraint = 100

    def __repr__(self):
        return str((self.a_btn, self.b_btn, self.prize))

    def winning_tokens(self) -> int:
        """compute lowest winning token combination"""

        # still trying to understand this. but took concept code
        # from rundavidrun @ reddit post:
        #
        # https://www.reddit.com/r/adventofcode/comments/1hd4wda/comment/m1temc7/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button
        #a = (c*y2 - d*x2) / (x1*y2 - y1*x2)
        #b = (d*x1 - c*y1) / (x1*y2 - y1*x2)

        px, py = map(int,self.prize)
        ax, ay = map(int,self.a_btn)
        bx, by = map(int,self.b_btn)

        a = (px * by - py * bx) / (ax * by - ay * bx)
        b = (py * ax - px * ay) / (ax * by - ay * bx)

        if int(a) == a and int(b) == b:
            return (int(a) * 3) + int(b)
        return 0

btn_extract = re.compile(r'Button [A|B]: X\+([0-9]+), Y\+([0-9]+)')
prize_extract = re.compile(r'Prize: X=([0-9]+), Y=([0-9]+)')

def parse_machines(lines: list[str]) -> list[PrizeMachine]:
    """parse prize machines from input"""
    machines = []
    for i in range(0, len(lines), 4):
        a = btn_extract.search(lines[i])
        a_btn = (int(a.group(1)), int(a.group(2)))
        b = btn_extract.search(lines[i+1])
        b_btn = (int(b.group(1)), int(b.group(2)))
        p = prize_extract.search(lines[i+2])
        prize = (int(p.group(1)), int(p.group(2)))
        machines.append(PrizeMachine(a_btn, b_btn, prize))
    return machines

# Data
data = read_lines("input/day13/input.txt")
sample = """Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279""".splitlines()

# Part 1
assert solve_part1(sample) == 480
assert solve_part1(data) == 36838

# Part 2
assert solve_part2(sample) == 875318608908
assert solve_part2(data) == 83029436920891
