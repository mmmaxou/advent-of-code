import os
from collections import Counter

inputPath = os.path.join(os.path.dirname(__file__), "input")

with open(inputPath, "r") as inputFile:
    lines = [line.replace("\n", "") for line in inputFile.readlines()]


def createGrid(height=10, width=10):
    return [[0 for y in range(width)] for x in range(height)]


def parseLine(line):
    coords = line.split(" -> ")
    return [list(map(int, coords[0].split(","))), list(map(int, coords[1].split(",")))]


def getDeviation(nums):
    return [nums[1][0] - nums[0][0], nums[1][1] - nums[0][1]]


def getStride(num):
    return 1 if num > 0 else -1 if num < 0 else 0


def getIncreasedGridValue(value):
    return value + 1


def getRangeIterator(start, deviation, i):
    try:
        stride = getStride(deviation[i])
        return range(start[i], start[i] + deviation[i] + stride, stride)
    except ValueError:
        return [start[i]]


def printGrid(grid):
    for line in grid:
        lineStr = "".join(map(str, line)).replace("0", ".")
        print(lineStr)


def countOverlap(grid, minOverlap=2):
    linesSumOverlap = []
    for line in grid:
        notOverlap = [Counter(line)[i] for i in range(minOverlap)]
        linesSumOverlap.append(len(line) - sum(notOverlap))
    return sum(linesSumOverlap)


def isDiagonalLine(deviation):
    if deviation[0] == 0 or deviation[1] == 0:
        return False
    if abs(deviation[0]) != abs(deviation[1]):
        return False
    return True


def answer(lines, noDiagonal=True, gridSize=10):
    grid = createGrid(gridSize, gridSize)

    for line in lines:
        start, end = parseLine(line)
        deviation = getDeviation([start, end])

        diagonalLine = isDiagonalLine(deviation)

        if noDiagonal and diagonalLine:
            continue

        for i, col in enumerate(getRangeIterator(start, deviation, 0)):
            for j, row in enumerate(getRangeIterator(start, deviation, 1)):
                if not diagonalLine or (i == j):
                    grid[row][col] = getIncreasedGridValue(grid[row][col])

    overlap = countOverlap(grid)
    # printGrid(grid)
    return overlap


gridSize = 1000
print(answer(lines, gridSize=gridSize))
print(answer(lines, noDiagonal=False, gridSize=gridSize))
