import os
import copy
from typing import Set
from collections import defaultdict


inputPath = os.path.join(os.path.dirname(__file__), "input")

with open(inputPath, "r") as inputFile:
    lines = [line.strip() for line in inputFile.readlines() if line.strip()]


class Pos:
    def __init__(self, x: int, y: int, z: int) -> None:
        self.x = x
        self.y = y
        self.z = z

    def neighbours(self, reach=1, includeSelf=False):
        if includeSelf:
            for zi in range(-reach, reach + 1, 1):
                for yi in range(-reach, reach + 1, 1):
                    for xi in range(-reach, reach + 1, 1):
                        yield Pos(self.x + xi, self.y + yi, self.z + zi)
        else:
            for zi in range(-reach, reach + 1, 1):
                for yi in range(-reach, reach + 1, 1):
                    for xi in range(-reach, reach + 1, 1):
                        if not (zi == 0 and yi == 0 and xi == 0):
                            yield Pos(self.x + xi, self.y + yi, self.z + zi)

    def __hash__(self) -> int:
        return hash(repr(self))

    def __eq__(self, o) -> bool:
        return self.x == o.x and self.y == o.y and self.z == o.z

    def __str__(self) -> str:
        return "(%s,%s,%s)" % (self.x, self.y, self.z)

    __repr__ = __str__


class HyperPos(Pos):
    def __init__(self, x: int, y: int, z: int, w: int) -> None:
        super(HyperPos, self).__init__(x, y, z)
        self.w = w

    def neighbours(self, reach=1, includeSelf=False):
        if includeSelf:
            for zi in range(-reach, reach + 1, 1):
                for yi in range(-reach, reach + 1, 1):
                    for xi in range(-reach, reach + 1, 1):
                        for wi in range(-reach, reach + 1, 1):
                            yield HyperPos(self.x + xi, self.y + yi, self.z + zi, self.w + wi)
        else:
            for zi in range(-reach, reach + 1, 1):
                for yi in range(-reach, reach + 1, 1):
                    for xi in range(-reach, reach + 1, 1):
                        for wi in range(-reach, reach + 1, 1):
                            if not (zi == 0 and yi == 0 and xi == 0 and wi == 0):
                                yield HyperPos(self.x + xi, self.y + yi, self.z + zi, self.w + wi)

    def __hash__(self) -> int:
        return hash(repr(self))

    def __eq__(self, o) -> bool:
        return self.x == o.x and self.y == o.y and self.z == o.z and self.w == o.w

    def __str__(self) -> str:
        return "(%s,%s,%s,%s)" % (self.x, self.y, self.z, self.w)

    __repr__ = __str__


class Dimension:
    def __init__(self, cubes: Set[Pos]):
        self.cubes = cubes

    @staticmethod
    def FromLines(lines):
        cubes: Set[Pos] = set()
        for y, line in enumerate(lines):
            for x, char in enumerate(list(line)):
                active = char == "#"
                if active:
                    pos = Pos(x, y, 0)
                    cubes.add(pos)
        return Dimension(cubes)

    def neighbourhood(self) -> Set[Pos]:
        neighbourhood = set()
        for cube in self.cubes:
            for neighbour in cube.neighbours(reach=1, includeSelf=True):
                neighbourhood.add(neighbour)
        return neighbourhood

    def isActive(self, pos: Pos) -> bool:
        return pos in self.cubes

    def neighboursActiveInRange(self, pos: Pos, min=None, max=None):
        activeNeighbours = 0
        for neighbour in pos.neighbours(reach=1):
            if self.isActive(neighbour):
                activeNeighbours += 1
                if activeNeighbours > max:
                    return False
        return activeNeighbours >= min

    def firstRule(self, cube: Pos) -> bool:
        """Return True if the cube shall be activated by the first rule:
        The cube must be active.
        If exactly 2 or 3 neighbors are active, the cube remains active.
        Otherwise, the cube becomes inactive.
        """
        assert self.isActive(cube)
        return self.neighboursActiveInRange(cube, min=2, max=3)

    def secondRule(self, cube: Pos) -> bool:
        """Return True if the cube shall be activated by the second rule:
        The cube must be inactive.
        If exactly 3 neighbors are active, the cube becomes active.
        Otherwise, the cube remains inactive.
        """
        assert not self.isActive(cube)
        return self.neighboursActiveInRange(cube, min=3, max=3)

    def layer(self, z: int) -> str:
        radius = len(lines[0]) * 2
        center = int((len(lines[0])) / 2)
        cubes = [["." for i in range(radius)] for i in range(radius)]
        for cube in [c for c in self.cubes if c.z == z]:
            cubes[cube.y + center][cube.x + center] = "#"
        return "\n".join("".join(c) for c in cubes)

    def cycle(self):
        buffer = set()
        for pos in self.neighbourhood():
            if self.isActive(pos):
                if self.firstRule(pos):
                    buffer.add(pos)
            else:
                if self.secondRule(pos):
                    buffer.add(pos)
        self.cubes = copy.deepcopy(buffer)


class HyperDimension(Dimension):
    @staticmethod
    def FromLines(lines):
        cubes: Set[HyperPos] = set()
        for y, line in enumerate(lines):
            for x, char in enumerate(list(line)):
                active = char == "#"
                if active:
                    pos = HyperPos(x, y, 0, 0)
                    cubes.add(pos)
        return HyperDimension(cubes)

    def layer(self, z: int, w: int) -> str:
        radius = len(lines[0]) * 2
        center = int((len(lines[0])) / 2)
        cubes = [["." for i in range(radius)] for i in range(radius)]
        for cube in [c for c in self.cubes if c.z == z and c.w == w]:
            cubes[cube.y + center][cube.x + center] = "#"
        return "\n".join("".join(c) for c in cubes)

    def cycle(self):
        buffer = set()
        for pos in self.neighbourhood():
            if self.isActive(pos):
                if self.firstRule(pos):
                    buffer.add(pos)
            else:
                if self.secondRule(pos):
                    buffer.add(pos)
        self.cubes = copy.deepcopy(buffer)


def solve1():
    dim = Dimension.FromLines(lines)
    print(dim.layer(0))
    dim.cycle()
    dim.cycle()
    dim.cycle()
    dim.cycle()
    dim.cycle()
    dim.cycle()
    return len(dim.cubes)


def solve2():
    dim = HyperDimension.FromLines(lines)
    print(dim.layer(0, 0))
    dim.cycle()
    dim.cycle()
    dim.cycle()
    dim.cycle()
    dim.cycle()
    dim.cycle()
    return len(dim.cubes)


print(solve1())
print(solve2())
