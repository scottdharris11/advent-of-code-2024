"""utility imports"""
from utilities.data import read_lines
from utilities.runner import runner

@runner("Day 24", "Part 1")
def solve_part1(lines: list[str]) -> int:
    """part 1 solving function"""
    wires, sidx = parse_wires(lines)
    gates = parse_gates(lines[sidx:])
    execute_gates(wires, gates)
    output, _ = value_from_bits(wires, 'z')
    return output

@runner("Day 24", "Part 2")
def solve_part2(lines: list[str]) -> str:
    """part 2 solving function"""
    wires, sidx = parse_wires(lines)
    gates = parse_gates(lines[sidx:])
    x, _ = value_from_bits(wires, 'x')
    y, _ = value_from_bits(wires, 'y')
    execute_gates(wires, gates)
    actual, zcnt = value_from_bits(wires, 'z')
    expected = x & y
    expected_bits = value_to_bits(expected, zcnt)
    actual_bits = value_to_bits(actual, zcnt)

    gates_by_output = {}
    for i, gate in enumerate(gates):
        gates_by_output[gate.outwire] = i

    swap_candidates = {}
    for i, b in enumerate(expected_bits):
        if b == actual_bits[i]:
            continue
        gi = gates_by_output['z' + str(i).zfill(2)]
        sc = swap_candidates.get(actual_bits[i],set())
        sc.add(gi)
        swap_candidates[actual_bits[i]] = sc
        swap_impact(gates[gi], gates, gates_by_output, swap_candidates, wires)

    print((len(swap_candidates[0]),len(swap_candidates[1])))
    return "not done yet"

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
        self.output = out
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

def execute_gates(wires: dict[str,int], gates: list[Gate]):
    """execute gates until all have completed"""
    while True:
        alldone = True
        for gate in gates:
            if not gate.execute(wires):
                alldone = False
        if alldone:
            break

def value_from_bits(wires: dict[str,int], prefix: chr) -> tuple[int,int]:
    """compute value from bits with supplied prefix"""
    output = 0
    count = 0
    for wire, value in wires.items():
        if wire[0] != prefix:
            continue
        count += 1
        if value == 0:
            continue
        shift = int(wire[1:])
        svalue = 1 << shift
        output |= svalue
    return output, count

def value_to_bits(value: int, bit_count:int) -> list[int]:
    """convert a value into array of bits"""
    bits = []
    for i in range(bit_count):
        work = value >> i
        bits.append(work & 1)
    return bits

def swap_impact(gate: Gate, gates: list[Gate], gates_by_output: dict[str,int], swap: dict[int,set[int]], wires: dict[str,int]):
    """recursively find swap impacts"""
    if gate.inwire1[0] != 'x' and gate.inwire1[0] != 'y' and gate.inwire1 not in swap:
        idx = gates_by_output[gate.inwire1]
        s = swap.get(wires[gate.inwire1], set())
        s.add(idx)
        swap[wires[gate.inwire1]] = s
        swap_impact(gates[idx], gates, gates_by_output, swap, wires)
    if gate.inwire2[0] != 'x' and gate.inwire2[0] != 'y' and gate.inwire2 not in swap:
        idx = gates_by_output[gate.inwire2]
        s = swap.get(wires[gate.inwire2], set())
        s.add(idx)
        swap[wires[gate.inwire2]] = s
        swap_impact(gates[idx], gates, gates_by_output, swap, wires)

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
sample3 = """x00: 0
x01: 1
x02: 0
x03: 1
x04: 0
x05: 1
y00: 0
y01: 0
y02: 1
y03: 1
y04: 0
y05: 1

x00 AND y00 -> z05
x01 AND y01 -> z02
x02 AND y02 -> z01
x03 AND y03 -> z03
x04 AND y04 -> z04
x05 AND y05 -> z00""".splitlines()

assert value_to_bits(11, 4) == [1,1,0,1]
assert value_to_bits(13, 4) == [1,0,1,1]

# Part 1
assert solve_part1(sample) == 4
assert solve_part1(sample2) == 2024
assert solve_part1(data) == 59336987801432

# Part 2
#assert solve_part2(sample3) == "z00,z01,z02,z05"
assert solve_part2(data) == ""
