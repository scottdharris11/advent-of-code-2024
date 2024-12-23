"""utility imports"""
from utilities.data import read_lines
from utilities.runner import runner

@runner("Day 23", "Part 1")
def solve_part1(lines: list[str]) -> int:
    """part 1 solving function"""
    connections = build_connections(lines)
    checked = set()
    lan_parties = set()
    for key, aconns in connections.items():
        checked.add(key)
        for aconn in aconns:
            # for each connection that a computer A has, see if
            # computer B has a connection that computer A has (not itself)
            if aconn in checked:
                continue
            for bconn in connections[aconn]:
                if bconn == key:
                    continue
                if bconn in aconns:
                    party = {key, aconn, bconn}
                    if key[0] == 't' or aconn[0] == 't' or bconn[0] == 't':
                        lan_parties.add(frozenset(party))
    return len(lan_parties)

@runner("Day 23", "Part 2")
def solve_part2(lines: list[str]) -> str:
    """part 2 solving function"""
    connections = build_connections(lines)
    checked = set()
    max_party = None
    for computer in connections:
        checked.add(computer)
        party = {computer}
        build_party(connections, party, computer, checked)
        if len(party) >= 3:
            if max_party is None or len(party) > len(max_party):
                max_party = party
    pl = list(max_party)
    pl.sort()
    return ",".join(pl)

def build_connections(lines: list[str]) -> dict[str,set[str]]:
    """build set of connections between computers"""
    connections = {}
    for line in lines:
        comps = line.split("-")
        compc = connections.get(comps[0], set())
        compc.add(comps[1])
        connections[comps[0]] = compc
        compc = connections.get(comps[1], set())
        compc.add(comps[0])
        connections[comps[1]] = compc
    return connections

def build_party(connections: dict[str,set[str]], party: set[str], comp: str, checked: set[str]):
    """build set of connected party"""
    for conn in connections[comp]:
        if conn in checked:
            continue
        allconnected = True
        for pconn in party:
            if conn not in connections[pconn]:
                allconnected = False
                break
        if allconnected:
            party.add(conn)
            for nc in connections[conn]:
                if nc in party:
                    continue
                build_party(connections, party, nc, checked)

# Data
data = read_lines("input/day23/input.txt")
sample = """kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn""".splitlines()

# Part 1
assert solve_part1(sample) == 7
assert solve_part1(data) == 1218

# Part 2
assert solve_part2(sample) == "co,de,ka,ta"
assert solve_part2(data) == "ah,ap,ek,fj,fr,jt,ka,ln,me,mp,qa,ql,zg"
