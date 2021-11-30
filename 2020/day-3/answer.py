import os


TREE = "#"
OPEN = "."

inputPath = os.path.join(os.path.dirname(__file__), "input")
with open(inputPath, "r") as inputFile:
    area = [list(line.strip()) for line in inputFile.readlines() if line]
    width = len(area[0])
    height = len(area)


def getLetterAt(x, y):
    if x < 0 or y < 0 or y >= height:
        return None
    return area[y][x % width]


def descend(right, down):
    x = 0
    y = 0
    outOfBound = False
    trees = 0
    while not outOfBound:
        position = getLetterAt(x, y)
        if position is None:
            outOfBound = True
        else:
            x += right
            y += down
            if position == TREE:
                trees += 1
    return trees


def solve():
    return descend(1, 1) * descend(3, 1) * descend(5, 1) * descend(7, 1) * descend(1, 2)


print(solve())
