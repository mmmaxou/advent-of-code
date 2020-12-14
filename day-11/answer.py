import os
import copy
from time import sleep
from typing import Tuple

TILE_FLOOR = "."
TILE_SEAT_EMPTY = "L"
TILE_SEAT_FULL = "#"
TILE_SEATS = [TILE_SEAT_EMPTY, TILE_SEAT_FULL]

inputPath = os.path.join(os.path.dirname(__file__), "input")

with open(inputPath, "r") as inputFile:
    initialLines = [line.strip() for line in inputFile.readlines() if line.strip()]


class Grid:
    def __init__(self, lines) -> None:
        """Assume lines is not null"""
        self.tiles = [[tile for tile in list(line)] for line in lines]
        self.buffer = [[tile for tile in list(line)] for line in lines]
        self.seats = []
        for j, line in enumerate(lines):
            for i, tile in enumerate(list(line)):
                if tile in TILE_SEATS:
                    self.seats.append((i, j))
        self.height = len(self.tiles)
        self.width = len(self.tiles[0])

    def swapBuffers(self):
        self.tiles = copy.deepcopy(self.buffer)
        self.buffer = copy.deepcopy(self.tiles)

    def displayTile(self, x, y):
        tmp = self.tiles[y][x]
        self.tiles[y][x] = "o"
        changed = str(self)
        print(changed)
        self.tiles[y][x] = tmp
        return changed

    def isInside(self, x, y):
        return x < self.width and x >= 0 and y < self.height and y >= 0

    def neighbors(self, x, y, reach=1):
        """Assume we are using the 8-adjacency"""
        around = 2 * reach + 1
        neighbors = []
        for i in range(around):
            X = i + x - 1
            for j in range(around):
                Y = j + y - 1
                if self.isInside(X, Y) and not (X == x and Y == y):
                    neighbors.append(self.tiles[Y][X])
        return neighbors

    def firstRule(self, x, y, reach=1):
        assert self.tiles[y][x] == TILE_SEAT_EMPTY
        occupied = [tile for tile in self.neighbors(x, y, reach) if tile == TILE_SEAT_FULL]
        return not occupied

    def secondRule(self, x, y, reach=1):
        assert self.tiles[y][x] == TILE_SEAT_FULL
        occupied = [tile for tile in self.neighbors(x, y, reach) if tile == TILE_SEAT_FULL]
        return len(occupied) >= 4

    def applyRules(self):
        madeChanges = False
        for x, y in self.seats:
            if self.tiles[y][x] == TILE_SEAT_EMPTY and self.firstRule(x, y, 1):
                self.buffer[y][x] = TILE_SEAT_FULL
                madeChanges = True
            elif self.tiles[y][x] == TILE_SEAT_FULL and self.secondRule(x, y, 1):
                self.buffer[y][x] = TILE_SEAT_EMPTY
                madeChanges = True
        self.swapBuffers()
        return madeChanges

    def seatsOccupied(self):
        return len([1 for x, y in self.seats if self.tiles[y][x] == TILE_SEAT_FULL])

    def __str__(self) -> str:
        return "\n".join(
            ["(H: %s, W:%s)" % (self.height, self.width)] + ["".join(row) for row in self.tiles] + ["-" * self.width]
        )

    __repr__ = __str__


class CastIterator:
    def __init__(self, grid, x, y, i, j):
        self.grid: Grid = grid
        self.x = x
        self.y = y
        self.i = i
        self.j = j
        self.index = 1

    def __iter__(self):
        return self

    def __next__(self):
        X = self.x + self.i * self.index
        Y = self.y + self.j * self.index
        self.index += 1
        if self.grid.isInside(X, Y):
            return (X, Y)
        raise StopIteration()


class Grid2(Grid):
    def __init__(self, lines) -> None:
        super(Grid2, self).__init__(lines)

    def castFrom(self, x, y, i, j):
        cast = CastIterator(self, x, y, i, j)
        for x, y in cast:
            if self.tiles[y][x] in TILE_SEATS:
                return x, y

    def neighbors(self, x, y, reach=1):
        """Assume we are using the 8-adjacency"""
        around = 2 * reach + 1
        neighbors = []
        for i in range(around):
            castI = i - 1
            for j in range(around):
                castJ = j - 1
                if not (castI == 0 and castJ == 0):
                    inSight = self.castFrom(x, y, castI, castJ)
                    if inSight:
                        X, Y = inSight
                        neighbors.append(self.tiles[Y][X])

        return neighbors

    def secondRule(self, x, y, reach=1):
        assert self.tiles[y][x] == TILE_SEAT_FULL
        occupied = [tile for tile in self.neighbors(x, y, reach) if tile == TILE_SEAT_FULL]
        return len(occupied) >= 5


def solve1():
    grid = Grid(initialLines)
    while grid.applyRules():
        pass
    return grid.seatsOccupied()


def solve2():
    grid = Grid2(initialLines)
    while grid.applyRules():
        pass
    return grid.seatsOccupied()


print(solve1())
print(solve2())
