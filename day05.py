"""utility imports"""
from utilities.data import read_lines
from utilities.runner import runner

@runner("Day 5", "Part 1")
def solve_part1(lines: list):
    """part 1 solving function"""
    rule_break = lines.index("")
    rules = parse_rules(lines[0:rule_break])
    total = 0
    for update in lines[rule_break+1:]:
        valid, middle = check_update(rules, list(map(int, update.split(","))))
        if valid:
            total += middle
    return total

@runner("Day 5", "Part 2")
def solve_part2(lines: list):
    """part 2 solving function"""
    return 0

class PageRule:
    """holds before/after rules for a particular page number"""
    def __init__(self) -> None:
        self.before = []
        self.after = []

    def __repr__(self):
        return str((self.before, self.after))

def parse_rules(lines: list[str]) -> dict[int,PageRule]:
    """create dict of rules by page number"""
    rules_by_page = {}
    for line in lines:
        before, after = map(int,line.split("|"))
        br = rules_by_page.get(before, PageRule())
        br.after.append(after)
        rules_by_page[before] = br
        ar = rules_by_page.get(after, PageRule())
        ar.before.append(before)
        rules_by_page[after] = ar
    return rules_by_page

def check_update(rules: dict[int,PageRule], order: list[int]) -> (bool, int):
    """determine if update is valid and middle number of it if so"""
    for i, page in enumerate(order):
        rule = rules[page]
        for b in order[:i]:
            if b not in rule.before:
                return (False, 0)
        for a in order[i+1:]:
            if a not in rule.after:
                return (False, 0)
    return (True, order[int(len(order)/2)])

# Data
data = read_lines("input/day05/input.txt")
sample = """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
""".splitlines()

# Part 1
assert solve_part1(sample) == 143
assert solve_part1(data) == 5588

# Part 2
assert solve_part2(sample) == 0
assert solve_part2(data) == 0
