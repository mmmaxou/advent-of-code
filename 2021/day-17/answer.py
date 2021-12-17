import collections
from itertools import product
import re
import os

with open(os.path.join(os.path.dirname(__file__), "input"), "r") as inputFile:
    inputString = [line.replace("\n", "") for line in inputFile.readlines()]


def getGoalBounds(line):
    return list(map(int, re.findall(r"-?\d+", line)))


def getMaxHeight(vx):
    return vx * (vx + 1) // 2


class Probe:
    def __init__(self, vx, vy) -> None:
        self.x = 0
        self.y = 0
        self.vx = vx
        self.vy = vy
        self.positions = {(self.x, self.y)}

    def move(self):
        self.x += self.vx
        self.y += self.vy
        self.vx = max(self.vx - 1, 0)
        self.vy -= 1
        self.positions.add((self.x, self.y))


def answer1(line):
    _, _, ymin, _ = getGoalBounds(line)
    return getMaxHeight(-ymin - 1)


def answer2(line):
    count = 0
    xmin, xmax, ymin, ymax = getGoalBounds(line)
    target = set(product(range(xmin, xmax + 1), range(ymin, ymax + 1)))
    vymax = answer1(line)
    vxmin = next(vx for vx in range(xmin) if xmin <= getMaxHeight(vx) <= xmax)
    for vx in range(vxmin, xmax + 1):
        for vy in range(ymin, vymax + 1):
            probe = Probe(vx, vy)
            while probe.x <= xmax and probe.y >= ymin:
                probe.move()
            if probe.positions.intersection(target):
                count += 1
    return count


print(answer1(inputString[0]))
print(answer1(inputString[1]))
print(answer2(inputString[0]))
print(answer2(inputString[1]))
