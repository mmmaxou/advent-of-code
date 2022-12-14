from __future__ import annotations

import os
import sys

from math import prod
from dataclasses import dataclass, field
from typing import List, Callable

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from utils import Map, Point, iterateWithWindow, ALPHABET, ConsoleColorMap

with open(os.path.join(os.path.dirname(__file__), "input"), "r") as inputFile:
    rawInput = inputFile.read().split("\n")


LEVELS = {letter: index for index, letter in enumerate(ALPHABET)}
LEVELS["S"] = 0
LEVELS["E"] = 26


class HeightMap(Map):
    def __init__(self, letterMap: Map) -> None:
        super().__init__(letterMap.datas)
        self.letterMap = letterMap
        self.letterMap.console = ConsoleColorMap(self.letterMap)
        self.dataType = int
        self.start = next(p for p in letterMap if letterMap.get(p) == "S")
        self.end = next(p for p in letterMap if letterMap.get(p) == "E")
        for point in letterMap:
            self.edit(point, LEVELS.get(letterMap.get(point)))
        self.pointByDataValue = self.createPointsByDataValues()

    def floorUnder(self, level, display=True):
        pointsCurrentLevel = self.pointByDataValue[level]
        pointslevelUnder = self.pointByDataValue[level - 1]

        if display:
            for point in pointsCurrentLevel:
                self.letterMap.console.edit(point, ConsoleColorMap.Colors.PURPLE)
            for point in pointslevelUnder:
                self.letterMap.console.edit(point, ConsoleColorMap.Colors.BLUE)
            self.letterMap.console.display()
            self.letterMap.console.resetColors()

        for point in pointsCurrentLevel:
            neighbours = self.neighbours(point)
            reachableNeighbours = []

        pass


def answer(iterable):
    letterMap = Map(iterable)
    heightMap = HeightMap(letterMap)
    reachableFromTop = heightMap.floorUnder(26)

    return


print(answer(rawInput))
