import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils import Map, Point, iterateWithWindow


with open(os.path.join(os.path.dirname(__file__), "input"), "r") as inputFile:
    inputLines = [line.strip() for line in inputFile.readlines() if line]

MAP_SIZE_X = 40
MAP_SIZE_Y = 20


class Knot:
    def __init__(self, point, i) -> None:
        self.point = point
        self.dependant: Knot = None
        self.i = i

    def applyConstraints(self):
        if not self.dependant:
            return

        self.dist = self.dependant.point - self.point
        if abs(self.dist.x) == 2 or abs(self.dist.y) == 2:
            self.point.x += self.oneOrZero(self.dist.x)
            self.point.y += self.oneOrZero(self.dist.y)

    def oneOrZero(self, x):
        """Table of truth : -2=-1; -1=-1; 0=0; 1=1; 2=1"""
        return (2 * (x > 0) - 1) * abs(x != 0)

    def __repr__(self) -> str:
        return "{point}:{i}".format(point=self.point, i=self.i)

    def __add__(self, other):
        return Knot(self.x + other.x, self.y + other.y, self.i)

    def __sub__(self, other):
        return Knot(self.x - other.x, self.y - other.y, self.i)


class Simulation:
    @property
    def head(self):
        return self.knots[0]

    @property
    def tail(self):
        return self.knots[-1]

    def __init__(self, knots=2) -> None:
        self.start = Point(MAP_SIZE_X // 2, MAP_SIZE_Y // 2)
        self.knots = [Knot(Point(MAP_SIZE_X // 2, MAP_SIZE_Y // 2), i) for i in range(knots)]
        for a, b in iterateWithWindow(self.knots, windowSize=2):
            b.dependant = a
        self.visitedPositions = set()

    def parseLine(self, line):
        direction, amount = line.split(" ")
        amount = int(amount)

        # Opposite direction for this problem
        direction = {
            "D": Map.DIRECTIONS_4_NAMES.UP,
            "U": Map.DIRECTIONS_4_NAMES.DOWN,
            "R": Map.DIRECTIONS_4_NAMES.LEFT,
            "L": Map.DIRECTIONS_4_NAMES.RIGHT,
        }[direction]
        vector = Map.DIRECTIONS_4[direction]

        self.applyDirection(vector, amount)

    def applyDirection(self, vector, amount):
        for _ in range(amount):
            self.head.point += vector
            for knot in self.knots[1:]:
                knot.applyConstraints()
            self.visitedPositions.add(Point(self.tail.point.x, self.tail.point.y))
        self.printStatus()

    def printStatus(self):
        stateMap = Map(["." * MAP_SIZE_X] * MAP_SIZE_Y)
        stateMap.dataType = None
        stateMap.edit(self.start, "s")
        for i, knot in enumerate(self.knots):
            if stateMap.inMap(knot.point):
                stateMap.edit(knot.point, str(i))
        if stateMap.inMap(self.tail.point):
            stateMap.edit(self.tail.point, "T")
        if stateMap.inMap(self.head.point):
            stateMap.edit(self.head.point, "H")
        stateMap.printMap(reverse=True)

    def printVisitedPositions(self):
        stateMap = Map(["#" * MAP_SIZE_X] * MAP_SIZE_Y)
        stateMap.dataType = None
        stateMap.printMap(visiblePoints=self.visitedPositions, reverse=True)


def answer(iterable, knots):
    simulation = Simulation(knots)
    for line in iterable:
        simulation.parseLine(line)
    simulation.printVisitedPositions()
    return len(simulation.visitedPositions)


print(answer(inputLines, knots=2))
print(answer(inputLines, knots=10))
