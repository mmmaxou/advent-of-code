import os
from functools import reduce
from itertools import combinations
from typing import List

inputPath = os.path.join(os.path.dirname(__file__), "input")

with open(inputPath, "r") as inputFile:
    lines = [int(line) for line in inputFile.readlines() if line]


class CombinatorIterator:
    def __init__(self, combinator) -> None:
        super().__init__()
        self._combinator: Combinator = combinator
        self._index = 0

    def __next__(self) -> int:
        if self._index < len(self._combinator.lines) - self._combinator.preamble:
            combs = combinations(
                self._combinator.lines[self._index: self._index + self._combinator.preamble],
                self._combinator.factor)
            sums = set([self._combinator.sums.get(combination) for combination in combs])
            nextVal = self._combinator.lines[self._index + self._combinator.preamble]
            self._index += 1
            return sums, nextVal
        raise StopIteration


class Combinator:
    def __init__(self, lines, factor, preamble) -> None:
        super().__init__()
        self.lines: List[int] = lines
        self.factor: int = factor
        self.preamble: int = preamble
        self.sums = {i: sum(i) for i in combinations(lines, factor)}

    def __iter__(self) -> CombinatorIterator:
        return CombinatorIterator(self)


def solve1():
    combinator2 = Combinator(lines, 2, 25)
    for sums, nextVal in combinator2:
        if nextVal not in sums:
            return nextVal


def solve2():
    invalidNumber = solve1()
    i, j = 0, 0
    while i < len(lines):
        linesSum = 0
        while linesSum < invalidNumber and i + j < len(lines):
            linesSum += lines[i + j]
            j += 1
        if linesSum == invalidNumber:
            return min(lines[i: i+j]) + max(lines[i: i+j])
        i += 1
        j = 0


print(solve1())
print(solve2())
