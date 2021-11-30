import os
from collections import defaultdict

inputPath = os.path.join(os.path.dirname(__file__), "input")

with open(inputPath, "r") as inputFile:
    initialLines = [line.strip() for line in inputFile.readlines() if line.strip()]
    startingNumbers = [int(i) for i in initialLines[0].split(",")]


class Occurence:
    def __init__(self) -> None:
        self.turns = []

    def turn(self, turn) -> None:
        self.turns.append(turn)

    def nextNumber(self) -> int:
        if len(self.turns) < 2:
            return 0
        else:
            return self.turns[-1] - self.turns[-2]

    def __str__(self) -> str:
        return str(self.turns)

    __repr__ = __str__


class Solver:
    def __init__(self) -> None:
        self.occurences = defaultdict(Occurence)
        self.spoken = [None]
        self.currentTurn = 1

    @property
    def nextNumber(self) -> int:
        lastNumberSpoken = self.spoken[self.currentTurn - 1]
        return self.occurences[lastNumberSpoken].nextNumber()

    def processNumber(self, number):
        self.spoken.append(number)
        self.occurences[number].turn(self.currentTurn)
        self.currentTurn += 1

    def sayStartingNumbers(self) -> None:
        for number in startingNumbers:
            self.processNumber(number)

    def playNextTurn(self) -> None:
        self.processNumber(self.nextNumber)

    def playUntil(self, turn) -> None:
        while self.currentTurn < turn:
            self.playNextTurn()


def solve1():
    solver = Solver()
    solver.sayStartingNumbers()
    solver.playUntil(turn=2020)
    return solver.nextNumber


def solve2():
    solver = Solver()
    solver.sayStartingNumbers()
    solver.playUntil(turn=30000000)
    return solver.nextNumber


print(solve1())
print(solve2())
