from collections import defaultdict
from typing import List, Any
from enum import Enum
from copy import deepcopy

ALPHABET = "abcdefghijklmnopqrstuvwxyz"


class Point:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.tuple = (x, y)

    def __repr__(self) -> str:
        return "({x},{y})".format(x=self.x, y=self.y)

    __str__ = __repr__

    def __eq__(self, other) -> bool:
        return other.x == self.x and other.y == self.y

    def __hash__(self) -> int:
        return hash(self.tuple)

    def __iter__(self):
        return iter(self.tuple)

    def __lt__(self, other):
        return (other.x + other.y) <= (self.x + self.y)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    __radd__ = __add__


class Map:

    # Up Right Down Left
    class DIRECTIONS_4_NAMES(Enum):
        UP = 0  # Haut
        RIGHT = 1  # Droite
        DOWN = 2  # Base
        LEFT = 3  # Gauche

    DIRECTIONS_4 = {
        DIRECTIONS_4_NAMES.UP: Point(0, -1),
        DIRECTIONS_4_NAMES.RIGHT: Point(-1, 0),
        DIRECTIONS_4_NAMES.DOWN: Point(0, 1),
        DIRECTIONS_4_NAMES.LEFT: Point(1, 0),
    }

    def __init__(self, datas) -> None:
        self.pointIterator: List[Point] = None
        self.map: List[List[any]] = None
        self.datas = datas
        self.fillMap(datas)
        self.dataType = type(datas[0][0])

    def __iter__(self):
        return iter(self.pointIterator)

    def __repr__(self) -> str:
        return str("\n".join(["".join(map(str, line)) for line in self.map]))

    def __len__(self) -> int:
        return len(self.map[0]) * len(self.map)

    __str__ = __repr__

    def fillMap(self, datas) -> None:
        self.map = [list(line) for line in datas]
        self.pointIterator = []
        for i in range(len(self.map)):
            for j in range(len(self.map[0])):
                self.pointIterator.append(Point(j, i))

    def get(self, point) -> Any:
        if self.dataType:
            return self.dataType(self.map[point.y][point.x])
        else:
            return self.map[point.y][point.x]

    def edit(self, point, value) -> None:
        self.map[point.y][point.x] = value

    def inMap(self, point) -> bool:
        if point.x < 0 or point.x >= len(self.map[0]) or point.y < 0 or point.y >= len(self.map):
            return False
        return True

    def neighbours(self, point, adjacency=4, wrap=False, stride=1) -> List[Point]:
        allNeighbours = []
        # print("x=%s, y=%s, center=%s" % (point.x, point.y, self.get(point)))
        for i in range(-stride, stride + 1):
            for j in range(-stride, stride + 1):
                if i == 0 and j == 0:
                    continue
                if adjacency == 4 and (i != 0 and j != 0):
                    continue
                nPoint = Point(point.x + i, point.y + j)
                if wrap or self.inMap(nPoint):
                    allNeighbours.append(nPoint)
                    # print("coord=%s,%s ;val=%s" % (i, j, self.get(nPoint)))
        return allNeighbours

    def linesTowardEdges(self, point) -> List[List[Point]]:
        """Return a list of list of points towards the edge of the map."""
        surroundings = {}
        for directionName in self.DIRECTIONS_4_NAMES:
            direction = self.DIRECTIONS_4[directionName]
            surroundings[directionName] = self.lineTowardEdge(point, direction)
        return surroundings

    def lineTowardEdge(self, point, direction) -> List[Point]:
        """Return a list of points towards the edge of the map."""
        line = []
        newPoint = point + direction
        while self.inMap(newPoint):
            line.append(newPoint)
            newPoint = newPoint + direction
        return line

    def getPointsAtBorder(self, directionName) -> List[Point]:
        """return a list of points at the border of the map.
        It is the opposite of the direction.
        I.E.:
        Direction UP -> all points on bottom
        Direction DOWN -> all points on top
        ...
        """
        points = []
        if directionName is self.DIRECTIONS_4_NAMES.UP:
            for i in range(len(self.map[0])):
                points.append(Point(i, len(self.map) - 1))
        elif directionName is self.DIRECTIONS_4_NAMES.DOWN:
            for i in range(len(self.map[0])):
                points.append(Point(i, 0))
        elif directionName is self.DIRECTIONS_4_NAMES.LEFT:
            for i in range(len(self.map[0])):
                points.append(Point(0, i))
        elif directionName is self.DIRECTIONS_4_NAMES.RIGHT:
            for i in range(len(self.map[0])):
                points.append(Point(len(self.map[0]) - 1, i))
        return points

    def createPointsByDataValues(self):
        pointByDataValue = defaultdict(list)
        for point in self:
            pointByDataValue[self.get(point)].append(point)
        return pointByDataValue

    def printMap(self, visiblePoints=None, reverse=False):
        visiblePoints = visiblePoints or self.pointIterator
        print("")
        print("*" * len(self.map[0]))
        line = ""
        iterator = self.pointIterator[::-1] if reverse else self.pointIterator
        for point in iterator:
            if point in visiblePoints:
                line = str(self.get(point)) + line
            else:
                line = "." + line
            if len(line) == len(self.map[0]):
                print(line)
                line = ""
        print("*" * len(self.map[0]))
        print("")


class ConsoleColorMap(Map):

    """https://stackoverflow.com/a/21786287"""

    class Colors:
        HEADER = "\x1b[95m"
        RED = "\x1b[0;31;40m"
        GREEN = "\x1b[0;32;40m"
        YELLOW = "\x1b[0;33;40m"
        BLUE = "\x1b[0;34;40m"
        PURPLE = "\x1b[0;35;40m"
        CYAN = "\x1b[0;36;40m"
        ENDC = "\x1b[0m"
        BOLD = "\x1b[1m"
        UNDERLINE = "\x1b[4m"

    def __init__(self, parentMap: Map) -> None:
        super().__init__(deepcopy(parentMap.datas))
        self.parentMap = parentMap
        self.globalStyle = ""
        self.dataType = str
        self.resetColors()

    def resetColors(self):
        for point in self.pointIterator:
            self.edit(point, "")

    def display(self):
        lines = [""]
        currentLine = 0
        for point in self.parentMap.pointIterator:
            if point.y != currentLine:
                currentLine += 1
                lines.append("")

            style = self.get(point) or self.globalStyle
            char = str(self.parentMap.get(point))
            if style:
                char = style + char + self.Colors.ENDC
            lines[-1] += char

        for line in lines:
            print(line)

    def testColors(self):
        for color in [
            self.Colors.BLUE,
            self.Colors.RED,
            self.Colors.BOLD,
            self.Colors.YELLOW,
            self.Colors.CYAN,
            self.Colors.GREEN,
            self.Colors.PURPLE,
            self.Colors.UNDERLINE,
            self.Colors.HEADER,
        ]:
            self.globalStyle = color
            self.display()
        self.globalStyle = ""


def iterateNumberwise(iterable, n=2):
    return zip(*[iter(iterable)] * n)


def iterateWithWindow(iterable, windowSize=2):
    for i in range(len(iterable) - windowSize + 1):
        yield iterable[i : i + windowSize]


def truncateToZeroOneOrminuesOne(self, x):
    return (2 * (x > 0) - 1) * abs(x != 0)
