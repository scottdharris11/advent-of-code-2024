"""utility imports"""
from utilities.data import read_lines
from utilities.runner import runner

@runner("Day 15", "Part 1")
def solve_part1(lines: list[str]):
    """part 1 solving function"""
    s = lines.index("")
    w = Warehouse(lines[:s])
    #print(w)
    for iline in lines[s+1:]:
        for i in iline:
            #print("Move " + i + ":")
            w.move(i)
            #print(w)
    return w.gpssum()

@runner("Day 14", "Part 2")
def solve_part2(lines: list[str]):
    """part 2 solving function"""
    s = lines.index("")
    w = DoubleWarehouse(lines[:s])
    #print(w)
    for iline in lines[s+1:]:
        for i in iline:
            #print("Move " + i + ":")
            w.move(i)
            #print(w)
    return w.gpssum()

moves = {'^': (0,-1), 'v': (0,1), '>': (1,0), '<': (-1,0)}

class Warehouse:
    """Warehouse definition"""
    def __init__(self, lines: list[str]) -> None:
        self.height = len(lines)
        self.width = len(lines[0])
        self.robot = (0,0)
        self.boxes = set()
        self.walls = set()
        for y in range(self.height):
            for x in range(self.width):
                if lines[y][x] == '#':
                    self.walls.add((x,y))
                elif lines[y][x] == 'O':
                    self.boxes.add((x,y))
                elif lines[y][x] == '@':
                    self.robot = (x,y)

    def __repr__(self):
        lines = ""
        for y in range(self.height):
            for x in range(self.width):
                if (x, y) in self.walls:
                    lines += "#"
                elif (x, y) in self.boxes:
                    lines += "O"
                elif (x, y) == self.robot:
                    lines += "@"
                else:
                    lines += "."
            lines += "\n"
        return lines

    def move(self, d: chr) -> None:
        """attempt to move robot in supplied direction"""
        t = self.__newloc__(self.robot, d)
        if t in self.walls:
            return
        m = True
        if t in self.boxes:
            m = self.__movebox__(t, self.__newloc__(t,d), d)
        if m:
            self.robot = t
        return

    def __newloc__(self, f: tuple[int,int], d: chr) -> tuple[int,int]:
        """build new location from the supplied location and direction"""
        adjust = moves[d]
        return (f[0]+adjust[0], f[1]+adjust[1])

    def __movebox__(self, f: tuple[int,int], t: tuple[int,int], d: chr) -> bool:
        """attempt to move a box (down a chain if possible) from a loc to a loc"""
        if t in self.walls:
            return False
        m = True
        if t in self.boxes:
            m = self.__movebox__(t, self.__newloc__(t,d), d)
        if m:
            self.boxes.remove(f)
            self.boxes.add(t)
        return m

    def gpssum(self) -> int:
        """sum of all box gps coordinates"""
        gpss = 0
        for box in self.boxes:
            gpss += (100 * box[1]) + box[0]
        return gpss

class DoubleWarehouse:
    """Warehouse definition"""
    def __init__(self, lines: list[str]) -> None:
        self.height = len(lines)
        self.width = len(lines[0])
        self.robot = (0,0)
        self.lboxes = set()
        self.rboxes = set()
        self.walls = set()
        for y in range(self.height):
            for x in range(self.width):
                if lines[y][x] == '#':
                    self.walls.add((x*2,y))
                    self.walls.add((x*2+1,y))
                elif lines[y][x] == 'O':
                    self.lboxes.add((x*2,y))
                    self.rboxes.add((x*2+1,y))
                elif lines[y][x] == '@':
                    self.robot = (x*2,y)
        self.width *= 2

    def __repr__(self):
        lines = ""
        for y in range(self.height):
            for x in range(self.width):
                if (x, y) in self.walls:
                    lines += "#"
                elif (x, y) in self.lboxes:
                    lines += "["
                elif (x, y) in self.rboxes:
                    lines += "]"
                elif (x, y) == self.robot:
                    lines += "@"
                else:
                    lines += "."
            lines += "\n"
        return lines

    def move(self, d: chr) -> None:
        """attempt to move robot in supplied direction"""
        t = self.__newloc__(self.robot, d)
        if t in self.walls:
            return
        m = True
        boxmoves = []
        if t in self.lboxes:
            m = self.__canmove__(t, self.__newloc__(t,d), d, boxmoves)
        elif t in self.rboxes:
            fl = (t[0]-1,t[1])
            tl = self.__newloc__(fl, d)
            m = self.__canmove__(fl, tl, d, boxmoves)
        if m:
            for boxmove in boxmoves:
                fl = boxmove[0]
                self.lboxes.remove(fl)
                self.rboxes.remove((fl[0]+1, fl[1]))
            for boxmove in boxmoves:
                tl = boxmove[1]
                self.lboxes.add(tl)
                self.rboxes.add((tl[0]+1, tl[1]))
            self.robot = t
        return

    def __newloc__(self, f: tuple[int,int], d: chr) -> tuple[int,int]:
        """build new location from the supplied location and direction"""
        adjust = moves[d]
        return (f[0]+adjust[0], f[1]+adjust[1])

    def __canmove__(self, fl: tuple[int,int], tl: tuple[int,int], d: chr, boxmoves: list) -> bool:
        """check to see if boxes can move (down a chain if possible) from a loc to a loc"""
        fr = ((fl[0]+1), fl[1])
        tr = ((tl[0]+1), tl[1])
        if tl in self.walls or tr in self.walls:
            return False
        if tl in self.lboxes:
            if not self.__canmove__(tl, self.__newloc__(tl,d), d, boxmoves):
                return False
        elif tl != fr and tl in self.rboxes:
            fl2 = (tl[0]-1,tl[1])
            tl2 = self.__newloc__(fl2, d)
            if not self.__canmove__(fl2, tl2, d, boxmoves):
                return False
        if tr != fl and tr in self.lboxes:
            fl2 = tr
            tl2 = self.__newloc__(fl2, d)
            if not self.__canmove__(fl2, tl2, d, boxmoves):
                return False
        boxmoves.append((fl, tl))
        return True

    def gpssum(self) -> int:
        """sum of all box gps coordinates"""
        gpss = 0
        for box in self.lboxes:
            gpss += (100 * box[1]) + box[0]
        return gpss

# Data
data = read_lines("input/day15/input.txt")
sample = """########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<""".splitlines()
sample2 = """##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^""".splitlines()
sample3 = """#######
#...#.#
#.....#
#..OO@#
#..O..#
#.....#
#######

<vv<<^^<<^^""".splitlines()

# Part 1
assert solve_part1(sample) == 2028
assert solve_part1(sample2) == 10092
assert solve_part1(data) == 1383666

# Part 2
assert solve_part2(sample3) == 618
assert solve_part2(sample2) == 9021
assert solve_part2(data) == 0
