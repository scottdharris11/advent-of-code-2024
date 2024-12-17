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
    pgm = Program(lines)
    pgm.a = 0
    itr = len(pgm.opcodes)-1
    out_op_idx = 0
    while itr >= 0:
        oi = len(pgm.opcodes)-2
        while oi >= 0:
            if out_op_idx == 0 and pgm.opcodes[oi] == 5:
                out_op_idx = oi+1
            pgm.run_instruction(oi, oi+1, True)
            oi -= 2
        if itr > 0:
            prev = pgm.opcodes[itr-1]
            rval = pgm.combo_operand(out_op_idx)
            mod8 = rval % 8
            if mod8 != 0:
                if mod8 < prev:
                    prev += prev - mod8
                else:
                    prev += mod8 - prev
            rval += prev
            if pgm.opcodes[out_op_idx] == 4:
                pgm.a = rval
            elif pgm.opcodes[out_op_idx] == 5:
                pgm.b = rval
            elif pgm.opcodes[out_op_idx] == 6:
                pgm.c = rval
        itr -= 1
    return pgm.a

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
            oi = self.run_instruction(oi, oi+1, False)
        return ",".join([str(num) for num in self.output])

    def run_instruction(self, instr_idx: int, op_idx: int, reverse: bool) -> int:
        """run supplied instruction with supplied operand"""
        instr = self.opcodes[instr_idx]
        if instr == 0:
            if reverse:
                self.adv_r(self.combo_operand(op_idx))
            else:
                self.adv(self.combo_operand(op_idx))
        elif instr == 1:
            self.bxl(self.literal_operand(op_idx))
        elif instr == 2:
            if reverse:
                self.bst_r(self.combo_operand(op_idx))
            else:
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
            if reverse:
                self.bdv_r(self.combo_operand(op_idx))
            else:
                self.bdv(self.combo_operand(op_idx))
        elif instr == 7:
            if reverse:
                self.cdv_r(self.combo_operand(op_idx))
            else:
                self.cdv(self.combo_operand(op_idx))
        return instr_idx + 2

    def adv(self, operand: int):
        """adv instruction operation"""
        self.a = int(self.a / (2 ** operand))

    def adv_r(self, operand: int):
        """adv reverse instruction operation"""
        self.a *= (2 ** operand)

    def bxl(self, operand: int):
        """bxl instruction operation"""
        self.b ^= operand

    def bst(self, operand: int):
        """bst instruction operation"""
        self.b = operand % 8

    def bst_r(self, operand: int):
        """bst reverse instruction operation"""
        self.b = self.b + (operand * 8)

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

    def bdv_r(self, operand: int):
        """adv reverse instruction operation"""
        self.b = self.a * (2 ** operand)

    def cdv(self, operand: int):
        """bdv instruction operation"""
        self.c = int(self.a / (2 ** operand))

    def cdv_r(self, operand: int):
        """bdv instruction operation"""
        self.c = self.a * (2 ** operand)

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
sample3 = """Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0""".splitlines()

# Operation tests
#optest = Program(sample)
#optest.c = 9
#optest.opcodes = [2,6]
#optest.run_instruction(0,1)
#assert optest.b == 1

#optest = Program(sample2)
#assert optest.run_program() == "4,2,5,6,7,7,7,7,3,1,0"
#assert optest.a == 0

#optest.b = 29
#optest.opcodes = [1,7]
#optest.run_instruction(0,1)
#assert optest.b == 26

#optest.b = 2024
#optest.c = 43690
#optest.opcodes = [4,0]
#optest.run_instruction(0,1)
#assert optest.b == 44354

#optest = Program(sample3)
#optest.a = 117440
#optest.run_program()

# Part 1
#assert solve_part1(sample) == "4,6,3,5,6,3,5,2,1,0"
#assert solve_part1(data) == "7,3,1,3,6,3,6,0,2"

# Part 2
assert solve_part2(sample3) == 117440
assert solve_part2(data) == 0
