"""utility imports"""
import re
from utilities.data import read_lines
from utilities.runner import runner

@runner("Day 14", "Part 1")
def solve_part1(lines: list[str], size: tuple[int,int]):
    """part 1 solving function"""
    robots = []
    for line in lines:
        robots.append(Robot(line))
    for _ in range(100):
        for robot in robots:
            robot.move(size)
    hsplit = int(size[0]/2)
    vsplit = int(size[1]/2)
    quad_counts = [0,0,0,0]
    for robot in robots:
        if robot.loc[0] < hsplit and robot.loc[1] < vsplit:
            quad_counts[0] += 1
        elif robot.loc[0] > hsplit and robot.loc[1] < vsplit:
            quad_counts[1] += 1
        elif robot.loc[0] < hsplit and robot.loc[1] > vsplit:
            quad_counts[2] += 1
        elif robot.loc[0] > hsplit and robot.loc[1] > vsplit:
            quad_counts[3] += 1
    factor = 1
    for c in quad_counts:
        factor *= c
    return factor

@runner("Day 14", "Part 2")
def solve_part2(lines: list[str], size: tuple[int,int]):
    """part 2 solving function"""
    robots = []
    for line in lines:
        robots.append(Robot(line))
    for i in range(100):
        locs = set()
        for robot in robots:
            robot.move(size)
            locs.add(robot.loc)
        print("Second " + str(i+1))
        for y in range(size[1]):
            r = ""
            for x in range(size[0]):
                if (x, y) in locs:
                    r += "1"
                else:
                    r += "."
            print(r)
    return 0

robot_extract = re.compile(r'p=([0-9]+),([0-9]+) v=([0-9\-]+),([0-9\-]+)')

class Robot:
    """Robot definition"""
    def __init__(self, s: str) -> None:
        r = robot_extract.search(s)
        self.loc = (int(r.group(1)), int(r.group(2)))
        self.velocity = (int(r.group(3)), int(r.group(4)))

    def __repr__(self):
        return str((self.loc, self.velocity))

    def move(self, size: tuple[int, int]):
        """move robot based on velocity"""
        newx = self.loc[0] + self.velocity[0]
        while newx >= size[0]:
            newx -= size[0]
        while newx < 0:
            newx += size[0]
        newy = self.loc[1] + self.velocity[1]
        while newy >= size[1]:
            newy -= size[1]
        while newy < 0:
            newy += size[1]
        self.loc = (newx, newy)

# Data
data = read_lines("input/day14/input.txt")
sample = """p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3""".splitlines()

# Part 1
assert solve_part1(sample, (11, 7)) == 12
assert solve_part1(data, (101, 103)) == 230435667

# Part 2
assert solve_part2(data, (101, 103)) == 0
