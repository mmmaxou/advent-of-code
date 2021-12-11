import os
from typing import List

with open(os.path.join(os.path.dirname(__file__), "input"), "r") as inputFile:
    inputString = [list(map(int, line.replace("\n", ""))) for line in inputFile.readlines()]


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


class OctoMap(Map):
    def increasePoint(self, point):
        newValue = self.get(point) + 1
        self.edit(point, newValue)
        if newValue == 10:
            for neighbour in self.neighbours(point, adjacency=8):
                self.increasePoint(neighbour)

    def step(self):
        for point in self:
            self.increasePoint(point)
        flashes = 0
        for point in self:
            if self.get(point) > 9:
                flashes += 1
                self.edit(point, 0)
        return flashes


def answer1(lines):
    octopussies = OctoMap(lines)
    return sum(octopussies.step() for _ in range(100))


def answer2(lines):
    octopussies = OctoMap(lines)
    size = len(octopussies)
    index = 0
    while True:
        index += 1
        if octopussies.step() == size:
            return index


print(answer1(inputString))
print(answer2(inputString))
