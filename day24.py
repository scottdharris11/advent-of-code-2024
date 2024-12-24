"""utility imports"""
from utilities.data import read_lines
from utilities.runner import runner

@runner("Day 24", "Part 1")
def solve_part1(lines: list[str]) -> int:
    """part 1 solving function"""
    wires, sidx = parse_wires(lines)
    gates = parse_gates(lines[sidx:])
    while True:
        alldone = True
        for gate in gates:
            if not gate.execute(wires):
                alldone = False
        if alldone:
            break
    output = 0
    for wire, value in wires.items():
        if wire[0] != 'z' or value == 0:
            continue
        shift = int(wire[1:])
        svalue = 1 << shift
        output |= svalue
    return output

@runner("Day 24", "Part 2")
def solve_part2(lines: list[str]) -> str:
    """part 2 solving function"""
    return 0

class Gate:
    """represents a logic gate"""
    def __init__(self, s: str):
        pieces = s.split(" ")
        self.inwire1 = pieces[0]
        self.inwire2 = pieces[2]
        self.outwire = pieces[4]
        self.gate_type = pieces[1]
        self.executed = False
        self.output = None

    def execute(self, wires: dict[str,int]) -> bool:
        """execute a gate if both inputs available"""
        if self.executed:
            return True
        wire1 = wires.get(self.inwire1)
        wire2 = wires.get(self.inwire2)
        if wire1 is None or wire2 is None:
            return False
        out = None
        if self.gate_type == "AND":
            out = self.andgate(wire1, wire2)
        elif self.gate_type == "OR":
            out = self.orgate(wire1, wire2)
        else:
            out = self.xorgate(wire1, wire2)
        wires[self.outwire] = out
        self.executed = True
        return True

    def andgate(self, wire1: int, wire2: int) -> int:
        """evalute an 'and' gate"""
        if wire1 == 1 and wire2 == 1:
            return 1
        return 0

    def orgate(self, wire1: int, wire2: int) -> int:
        """evaluate an 'or' gate"""
        if wire1 == 1 or wire2 == 1:
            return 1
        return 0

    def xorgate(self, wire1: int, wire2: int) -> int:
        """evaluate an 'xor' gate"""
        if wire1 != wire2:
            return 1
        return 0

def parse_wires(lines: list[str]) -> tuple[dict[str,int],int]:
    """parse initial wire values"""
    wires = {}
    for i, l in enumerate(lines):
        if l == "":
            return wires, i+1
        pieces = l.split(": ")
        wires[pieces[0]] = int(pieces[1])
    return wires, len(lines)

def parse_gates(lines: list[str]) -> list[Gate]:
    """parse initial wire values"""
    gates = []
    for line in lines:
        gates.append(Gate(line))
    return gates

# Data
data = read_lines("input/day24/input.txt")
sample = """x00: 1
x01: 1
x02: 1
y00: 0
y01: 1
y02: 0

x00 AND y00 -> z00
x01 XOR y01 -> z01
x02 OR y02 -> z02""".splitlines()
sample2 = """x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj""".splitlines()

# Part 1
assert solve_part1(sample) == 4
assert solve_part1(sample2) == 2024
assert solve_part1(data) == 59336987801432

# Part 2
assert solve_part2(sample) == 0
assert solve_part2(data) == 0
