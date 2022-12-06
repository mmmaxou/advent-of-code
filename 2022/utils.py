from typing import List, Any


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
                self.pointIterator.append(Point(j, i))
        return newMap

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
