import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils import Map, Point


with open(os.path.join(os.path.dirname(__file__), "input"), "r") as inputFile:
    inputLines = [[int(x) for x in line.strip()] for line in inputFile.readlines() if line.strip()]


class TreeHeightMap(Map):
    def allVisibleTrees(self):

        # Get all points from border for each direction
        for directionName, direction in zip(self.DIRECTIONS_4_NAMES, self.DIRECTIONS_4):
            
            pass


def answer1(iterable):
    treeHeightMap = TreeHeightMap(iterable)
    return len(treeHeightMap.allVisibleTrees())


# def answer2(iterable):
#     allNodes = Parser().parse(iterable).root.visit(include, allNodes=[])["kwargs"]["allNodes"]
#     requiredSpace = 30000000 - (70000000 - max(allNodes))
#     allNodes = Parser().parse(iterable).root.visit(atLeast, value=requiredSpace, allNodes=[])["kwargs"]["allNodes"]
#     return min(allNodes)


print(answer1(inputLines))
# print(answer2(blocks))
