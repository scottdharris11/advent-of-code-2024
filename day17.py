"""utility imports"""
from utilities.data import read_lines, parse_integers
from utilities.runner import runner

@runner("Day 17", "Part 1")
def solve_part1(lines: list[str]) -> str:
    """part 1 solving function"""
    pgm = Program(lines)
    return pgm.run_program()

@runner("Day 17", "Part 2")
def solve_part2(lines: list[str]):
    """part 2 solving function"""
    return 0

class Program:
    """represents an operating program"""
    def __init__(self, lines: list[str]):
        self.a = int(lines[0][lines[0].index(":")+1:])
        self.b = int(lines[1][lines[1].index(":")+1:])
        self.c = int(lines[2][lines[2].index(":")+1:])
        self.opcodes = parse_integers(lines[4][lines[4].index(":")+1:],",")
        self.output = []

    def run_program(self) -> str:
        """run program from beginning to end"""
        self.output = []
        oi = 0
        while oi < len(self.opcodes)-1:
            oi = self.run_instruction(oi, oi+1)
        return ",".join([str(num) for num in self.output])

    def run_instruction(self, instr_idx: int, op_idx: int) -> int:
        """run supplied instruction with supplied operand"""
        instr = self.opcodes[instr_idx]
        if instr == 0:
            self.adv(self.combo_operand(op_idx))
        elif instr == 1:
            self.bxl(self.literal_operand(op_idx))
        elif instr == 2:
            self.bst(self.combo_operand(op_idx))
        elif instr == 3:
            r = self.jnz(self.literal_operand(op_idx))
            if r > -1:
                return r
        elif instr == 4:
            self.bxc()
        elif instr == 5:
            self.out(self.combo_operand(op_idx))
        elif instr == 6:
            self.bdv(self.combo_operand(op_idx))
        elif instr == 7:
            self.cdv(self.combo_operand(op_idx))
        return instr_idx + 2

    def adv(self, operand: int):
        """adv instruction operation"""
        self.a = int(self.a / (2 ** operand))

    def bxl(self, operand: int):
        """bxl instruction operation"""
        self.b ^= operand

    def bst(self, operand: int):
        """bst instruction operation"""
        self.b = operand % 8

    def jnz(self, operand: int) -> int:
        """jnz instruction operation"""
        if self.a == 0:
            return -1
        return operand

    def bxc(self):
        """bxc instruction operation"""
        self.b ^= self.c

    def out(self, operand: int):
        """out instruction operation"""
        self.output.append(operand % 8)

    def bdv(self, operand: int):
        """bdv instruction operation"""
        self.b = int(self.a / (2 ** operand))

    def cdv(self, operand: int):
        """bdv instruction operation"""
        self.c = int(self.a / (2 ** operand))

    def literal_operand(self, op_idx: int) -> int:
        """evaluate literal operand"""
        return self.opcodes[op_idx]

    def combo_operand(self, op_idx: int) -> int:
        """evaluate combo operand"""
        if self.opcodes[op_idx] < 4:
            return self.opcodes[op_idx]
        elif self.opcodes[op_idx] == 4:
            return self.a
        elif self.opcodes[op_idx] == 5:
            return self.b
        elif self.opcodes[op_idx] == 6:
            return self.c
        else:
            raise ValueError("Operand 7 is not valid")

# Data
data = read_lines("input/day17/input.txt")
sample = """Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0""".splitlines()
sample2 = """Register A: 2024
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0""".splitlines()

# Operation tests
optest = Program(sample)
optest.c = 9
optest.opcodes = [2,6]
optest.run_instruction(0,1)
assert optest.b == 1

optest = Program(sample2)
assert optest.run_program() == "4,2,5,6,7,7,7,7,3,1,0"
assert optest.a == 0

optest.b = 29
optest.opcodes = [1,7]
optest.run_instruction(0,1)
assert optest.b == 26

optest.b = 2024
optest.c = 43690
optest.opcodes = [4,0]
optest.run_instruction(0,1)
assert optest.b == 44354

# Part 1
assert solve_part1(sample) == "4,6,3,5,6,3,5,2,1,0"
assert solve_part1(data) == "7,3,1,3,6,3,6,0,2"

# Part 2
#assert solve_part2(sample) == 0
#assert solve_part2(data) == 0
