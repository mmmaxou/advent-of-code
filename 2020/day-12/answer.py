import os
import math

inputPath = os.path.join(os.path.dirname(__file__), "input")

with open(inputPath, "r") as inputFile:
    initialLines = [line.strip() for line in inputFile.readlines() if line.strip()]


class Pos:
    def __init__(self, x=0, y=0) -> None:
        self.x: int = x
        self.y: int = y

    @property
    def manhattanDistance(self) -> int:
        return abs(self.x) + abs(self.y)

    def __add__(self, other):
        assert isinstance(other, Pos)
        return Pos(self.x + other.x, self.y + other.y)

    __radd__ = __add__

    def __mul__(self, other):
        if isinstance(other, Pos):
            return Pos(self.x * other.x, self.y * other.y)
        elif isinstance(other, (float, int)):
            return Pos(self.x * other, self.y * other)

    __rmul__ = __mul__

    def __repr__(self):
        return "(%s, %s)" % (self.x, self.y)


def rotationMatrix(alpha):
    rads = math.radians(alpha)
    cos = int(math.cos(rads))
    sin = int(math.sin(rads))
    return [[cos, sin], [-1 * sin, cos]]


def matmul(A, B):
    return [[sum(a*b for a, b in zip(Arow, Bcol)) for Bcol in zip(*B) for Arow in A]]


EAST = Pos(1, 0)
WEST = Pos(-1, 0)
NORTH = Pos(0, 1)
SOUTH = Pos(0, -1)
DIRECTIONS = [NORTH, EAST, SOUTH, WEST]
GET_DIRECTION = {"N": NORTH, "S": SOUTH, "E": EAST, "W": WEST}
ROTATE = {"L": -1, "R": 1}


class Ship:
    def __init__(self) -> None:
        self.pos = Pos()

    def moveDirection(self, dir, val):
        self.pos += dir * val

    def __repr__(self):
        return "Pos: %s, Dist: %s" % (self.pos, self.pos.manhattanDistance)


class ShipWithDirection(Ship):
    def __init__(self) -> None:
        super().__init__()
        self.dirIndex = 1

    @property
    def direction(self) -> Pos:
        return DIRECTIONS[self.dirIndex % 4]

    def rotate(self, val) -> None:
        assert val % 90 == 0
        indexChange = int(val/90)
        self.dirIndex += indexChange

    def forward(self, val) -> None:
        self.pos += self.direction * val

    def __repr__(self):
        return super().__repr__() + ", Dir: %s" % self.direction


class Waypoint(Ship):
    def __init__(self) -> None:
        super().__init__()
        self.pos += EAST * 10
        self.pos += NORTH * 1

    def rotate(self, val):
        assert val % 90 == 0
        rotMatrix = rotationMatrix(val)
        rotatedVals = matmul(rotMatrix, [[self.pos.x], [self.pos.y]])
        x, y = map(int, rotatedVals[0])
        self.pos = Pos(x, y)

    def __repr__(self):
        return "Pos: %s" % (self.pos)


class Ship2(Ship):
    def __init__(self) -> None:
        super().__init__()
        self.waypoint = Waypoint()

    def moveDirection(self, dir, val) -> None:
        self.waypoint.moveDirection(dir, val)

    def rotate(self, val) -> None:
        self.waypoint.rotate(val)

    def forward(self, val):
        self.pos += self.waypoint.pos * val

    def __repr__(self):
        return super().__repr__() + ", Waypoint: (%s)" % (self.waypoint)


def solve1():
    ship = ShipWithDirection()
    for line in initialLines:
        command, value = (line[0], int(line[1:]))
        if command in GET_DIRECTION:
            direction = GET_DIRECTION[command]
            ship.moveDirection(direction, value)
        elif command in ROTATE:
            directionMult = ROTATE[command]
            ship.rotate(value * directionMult)
        elif command == "F":
            ship.forward(value)

    return ship.pos.manhattanDistance


def solve2():
    ship = Ship2()
    for line in initialLines:
        command, value = (line[0], int(line[1:]))
        if command in GET_DIRECTION:
            direction = GET_DIRECTION[command]
            ship.moveDirection(direction, value)
        elif command in ROTATE:
            directionMult = ROTATE[command]
            ship.rotate(value * directionMult)
        elif command == "F":
            ship.forward(value)

    return ship.pos.manhattanDistance


# print(solve1())
print(solve2())
