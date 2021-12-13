import os
import sys
import math
from functools import reduce

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils import Map, Point

with open(os.path.join(os.path.dirname(__file__), "input"), "r") as inputFile:
    inputString = [line.replace("\n", "") for line in inputFile.readlines()]
    pointsLines = [map(int, line.split(",")) for line in inputString if "," in line]
    points = {Point(x, y) for x, y in pointsLines}
    folds = [line.replace("fold along ", "").split("=") for line in inputString if line.startswith("fold")]


MAP_SIZE = 15


class TransparentPaper(Map):
    def __init__(self, points, size=None) -> None:
        if not size:
            size = Point(0, 0)
            for point in points:
                if point.x > size.x:
                    size.x = point.x
                if point.y > size.y:
                    size.y = point.y
            size.x += 1
            size.y += 1
        super().__init__(["." * size.x] * size.y)
        self.fillPoints(points)
        self.size = size

    def fillPoints(self, points):
        self.points = points
        for point in points:
            self.edit(point, "#")

    def fold(self, axis, center):
        newPoints = set()
        newSize = Point(self.size.x, self.size.y)
        if axis == "y":
            newSize.y = math.ceil(newSize.y / 2) + 1
            for point in self.points:
                if point.y < center:
                    newPoint = Point(point.x, point.y)
                else:
                    y = ((point.y - center) * -1) + center
                    newPoint = Point(point.x, y)
                newPoints.add(newPoint)
        if axis == "x":
            newSize.x = math.ceil(newSize.x / 2) + 1
            for point in self.points:
                if point.x < center:
                    newPoint = Point(point.x, point.y)
                else:
                    x = ((point.x - center) * -1) + center
                    newPoint = Point(x, point.y)
                newPoints.add(newPoint)
        return TransparentPaper(newPoints, newSize)


def nextFold(paper, fold):
    return paper.fold(fold[0], int(fold[1]))


def answer1():
    paper = TransparentPaper(points)
    folded = nextFold(paper, folds[0])
    return len(folded.points)


def answer2():
    paper = TransparentPaper(points)
    folded = reduce(nextFold, folds, paper)
    print(folded)

print(answer1())
print(answer2())
