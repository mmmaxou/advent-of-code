import os
import collections
import operator
from functools import reduce
from typing import List

with open(os.path.join(os.path.dirname(__file__), "input"), "r") as inputFile:
    inputString = [line.replace("\n", "") for line in inputFile.readlines()]


class Point:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return "({x},{y})".format(x=self.x, y=self.y)

    __str__ = __repr__

    def __eq__(self, __o: object) -> bool:
        return __o.x == self.x and __o.y == self.y

    def __hash__(self) -> int:
        return int(str(self.x).zfill(10) + str(self.y).zfill(10), 10)


class Map:
    def __init__(self, datas) -> None:
        self.pointIterator = None
        self.map = self.fillMap(datas)

    def __iter__(self):
        return iter(self.pointIterator)

    def __repr__(self) -> str:
        return str("\n".join(["".join(map(str, line)) for line in self.map]))

    def __len__(self) -> int:
        return len(self.map[0]) * len(self.map)

    __str__ = __repr__

    def fillMap(self, datas) -> None:
        newMap = [list(line) for line in datas]
        self.pointIterator = []
        for i in range(len(newMap)):
            for j in range(len(newMap[0])):
                self.pointIterator.append(Point(i, j))
        return newMap

    def get(self, point) -> int:
        return int(self.map[point.y][point.x])

    def edit(self, point, value) -> None:
        self.map[point.y][point.x] = value

    def inMap(self, point) -> bool:
        if point.x < 0 or point.x >= len(self.map[0]) or point.y < 0 or point.y >= len(self.map):
            return False
        return True

    def neighbours(self, point, adjacency=4, wrap=False) -> List[Point]:
        allNeighbours = []
        # print("x=%s, y=%s, center=%s" % (point.x, point.y, self.get(point)))
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                if adjacency == 4 and abs(i) == abs(j):
                    continue
                nPoint = Point(point.x + i, point.y + j)
                if wrap or self.inMap(nPoint):
                    allNeighbours.append(nPoint)
                    # print("coord=%s,%s ;val=%s" % (i, j, self.get(nPoint)))
        return allNeighbours

    def findLowerPointsCoords(self) -> List[Point]:
        lowPoints = []
        for x in range(len(self.map[0])):
            for y in range(len(self.map)):
                point = Point(x, y)
                value = self.get(point)
                neighboursValues = [self.get(nPoint) for nPoint in self.neighbours(point)]
                lowPoint = all([value < neighbourValue for neighbourValue in neighboursValues])
                if lowPoint:
                    lowPoints.append(point)
        return lowPoints

    def basin(self, point, adjacency=4, wrap=False) -> List[Point]:
        basin = [point]
        contours = collections.defaultdict(set)
        index = 0
        contours[0] = set(self.neighbours(point, adjacency, wrap))
        while contours[index] and index < 10:
            for nPoint in contours[index]:
                if (
                    self.get(point) < self.get(nPoint)
                    and self.get(nPoint) != 9
                    and nPoint not in basin
                    and nPoint not in contours[index + 1]
                ):
                        basin.append(nPoint)
                        contours[index + 1].update(self.neighbours(nPoint))
            index += 1
        return basin


def answer1(lines):
    heightMap = Map(lines)
    return sum([heightMap.get(point) + 1 for point in heightMap.findLowerPointsCoords()])


def answer2(lines):
    heightMap = Map(lines)
    basinsSizes = sorted([len(heightMap.basin(point)) for point in heightMap.findLowerPointsCoords()], reverse=True)
    return reduce(operator.mul, basinsSizes[0:3], 1)

print(answer1(inputString))
print(answer2(inputString))
