import os
import math
from collections import deque

inputPath = os.path.join(os.path.dirname(__file__), "input")

with open(inputPath, "r") as inputFile:
    lines = [line.strip() for line in inputFile.readlines() if line]


def findValue(lower, upper, letters, upperHalf="B", lowerHalf="F"):
    if len(letters) == 0:
        assert lower == upper
        return lower

    firstLetter = letters.popleft()

    mid = (upper - lower) / 2
    if firstLetter == upperHalf:
        lower += math.ceil(mid)
        return findValue(lower, upper, letters, upperHalf, lowerHalf)
    elif firstLetter == lowerHalf:
        upper -= math.ceil(mid)
        return findValue(lower, upper, letters, upperHalf, lowerHalf)


def findId(row, col):
    return row * 8 + col


def fullfillPlane():
    ids = [[0 for j in range(8)] for i in range(128)]
    for line in lines:
        row = findValue(0, 127, deque(line[:7]))
        col = findValue(0, 7, deque(line[7:]), "R", "L")
        id = findId(row, col)
        ids[row][col] = id
    return ids


def solve1():
    plane = fullfillPlane()
    return max([max(i) for i in plane])


def solve2():
    plane = fullfillPlane()

    # Simple visualisation of the array is enough here, but let's do code for fun
    last = 0
    for row in plane:
        for passenger in row:
            if passenger != 0:
                last = passenger
            else:
                if last != 0:
                    return last + 1


print(solve1())
print(solve2())
