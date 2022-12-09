from typing import List, Any
from enum import Enum

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
    
    __radd__ = __add__


class Map:

    # Up Right Down Left
    class DIRECTIONS_4_NAMES(Enum):
        UP = 0
        RIGHT = 1
        DOWN = 2
        LEFT = 3
    DIRECTIONS_4 = [Point(0, -1), Point(-1, 0), Point(0, 1), Point(1, 0)]

    def __init__(self, datas) -> None:
        self.pointIterator: List[Point] = None
        self.map: List[List[any]] = None
        self.fillMap(datas)

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
        return int(self.map[point.y][point.x])

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
        surroundings = [[] for _ in range(4)]
        for i, direction in enumerate(self.DIRECTIONS_4):
            newPoint = point + direction
            while self.inMap(newPoint):
                surroundings[i].append(newPoint)
                newPoint = newPoint + direction

        return surroundings


class Grid:
    def __init__(self, gridData) -> None:
        self.map = gridData
        self.max = Point(*map(max, zip(*self.map.keys())))

    def neighbours(self, point, adjacency=4, wrap=False, stride=1):
        allNeighbours = []
        for i in range(-stride, stride + 1):
            for j in range(-stride, stride + 1):
                if i == 0 and j == 0:
                    continue
                if adjacency == 4 and (i != 0 and j != 0):
                    continue
                newPoint = Point(point.x + i, point.y + j)

                if wrap:
                    newPoint.x = newPoint.x % self.max.x
                    newPoint.y = newPoint.y % self.max.y

                if newPoint in self.map:
                    allNeighbours.append(newPoint)

        return allNeighbours


def iterateNumberwise(iterable, n=2):
    return zip(*[iter(iterable)] * n)


def iterateWithWindow(iterable, windowSize=2):
    for i in range(len(iterable) - windowSize + 1):
        yield iterable[i: i + windowSize]
