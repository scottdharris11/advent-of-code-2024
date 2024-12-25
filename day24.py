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
    # After thinking about this for a while and having no clue
    # how to proceed since the combination of wires to switch
    # was way too emmense, i consulted hyperneutrino video on the
    # day which led me to not verifying the output, but verifying
    # the formula construction.  Since we are attempting to "add"
    # two values, the forumulas should be inline with binary addition
    # principles.  the tricky piece is dealing with the carry bits.
    # This will be my adaption of his solution with hopefully my
    # understanding of the approach and rationale. Check out his
    # video on the day here: https://www.youtube.com/watch?v=SU6lp6wyd3I
    #
    # Here are the rules we will be looking for to validate:
    #  1. starting with each zwire output, ensure that the wire is generated
    #     by an XOR since we only want a one when exactly one of the inputs
    #     is a 1.  0::0 would be 0 with no carry.  1::1 would be 0 with carry.
    #  2. if the zwire output is from a x/y wire (input wire), then it must
    #     align with the same level (e.g z01 would need to be x01/y01) since 
    #     that would be required for adding numbers properly.
    #  3. when not a x/y input, we need to look at each of the input wire
    #     formulaes to validate them.
    #  4. for positions after 0, the carry bit must be considered, so any direct
    #     usage of x/y input would be wrong.
    #  5. one side of the input formulaes should always be a "XOR" of the corresponding
    #     x/y input wires.  the other side will contain a formulae to represent the
    #     carry bit.
    #  6. carry bit case for position 1 is simple (should be AND of inputs x00 and y00)
    #     since it would only contain a value if both x00 and y00 were 1.
    #  7. carry bit for positions 2 and on will be...
    _, sidx = parse_wires(lines)
    gates = parse_gates(lines[sidx:])
    gbw = {}
    for gate in gates:
        gbw[gate.outwire] = gate

    print(pp(gbw, "z01", 0))
    print(pp(gbw, "z02", 0))
    print(pp(gbw, "z03", 0))

    for zidx in range(46):
        zwire = wire_name('z', zidx)
        validate_wire_gate(find_gate(gates, zwire), gates, 0)
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

    def __str__(self):
        return str((self.inwire1, self.gate_type, self.inwire2, " = ", self.outwire))

    def execute(self, wires: dict[str,int]) -> bool:
        """execute a gate if both inputs available"""
        if self.executed:
            return True
        wire1 = wires.get(self.inwire1)
        wire2 = wires.get(self.inwire2)
        if wire1 is None or wire2 is None:
            return False
        if self.gate_type == "AND":
            self.output = wire1 & wire2
        elif self.gate_type == "OR":
            self.output = wire1 | wire2
        else:
            self.output = wire1 ^ wire2
        wires[self.outwire] = self.output
        self.executed = True
        return True

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

def wire_name(prefix: chr, number: int) -> str:
    """convert prefix and wire number into wire name"""
    return prefix + str(number).zfill(2)

def find_gate(gates: list[Gate], outwire: str) -> Gate:
    """find the gate with the given outwire"""
    for gate in gates:
        if gate.outwire == outwire:
            return gate
    return None

def validate_wire_gate(gate: Gate, gates: list[Gate], level: int) -> bool:
    """validate the z output gate is correct"""
    # input gate into zwire must be an XOR since 0:0 would result
    # in zero and 1:1 would result in zero with a carry bit.  so, in
    # order to get the proper output, an xor gate is the only one
    # that will give the proper value (only one bit is on).
    if gate.gate_type != "XOR":
        print((gate.outwire, "not xor"))
        return False
    return True

def pp(gates: dict[str,Gate], wire: str, level: int) -> str:
    """print out a gate"""
    if wire[0] in "xy":
        return "  " * level + wire
    gate = gates[wire]
    return "  " * level + str(gate) + "\n" + \
           pp(gates, gate.inwire1, level + 1) + "\n" + \
           pp(gates, gate.inwire2, level + 1)

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
assert solve_part2(data) == ""
