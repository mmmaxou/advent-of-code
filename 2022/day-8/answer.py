import os
import sys

from math import prod

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils import Map, Point


with open(os.path.join(os.path.dirname(__file__), "input"), "r") as inputFile:
    inputLines = [[int(x) for x in line.strip()] for line in inputFile.readlines() if line.strip()]


class TreeHeightMap(Map):

    MAX_TREE_HEIGHT = 9

    def allVisibleTrees(self):

        visibleTrees = set()

        # Get all points from border for each direction
        for directionName in self.DIRECTIONS_4_NAMES:
            direction = self.DIRECTIONS_4[directionName]

            self.printVisibleTrees(visibleTrees)

            # Get all points at the border of the map.
            for treeAtBorder in self.getPointsAtBorder(directionName):

                tallestTreeInSight = self.get(treeAtBorder)
                visibleTrees.add(treeAtBorder)

                # For each point at the border create a range of points looking inside the tree map
                for treeInSigthPoint in self.lineTowardEdge(treeAtBorder, direction):

                    treeInSigthHeight = self.get(treeInSigthPoint)
                    if treeInSigthHeight > tallestTreeInSight:
                        tallestTreeInSight = treeInSigthHeight
                        visibleTrees.add(treeInSigthPoint)

                    if tallestTreeInSight == self.MAX_TREE_HEIGHT:
                        break

        self.printVisibleTrees(visibleTrees)

        return visibleTrees

    def allScenicScores(self):
        allScenicScores = {}
        for treeCenterPoint in self:
            treeCenterHeight = self.get(treeCenterPoint)
            inSigth = {}
            for direction, sightLine in self.linesTowardEdges(treeCenterPoint).items():
                inSightOneDirection = set()
                for treeInSightPoint in sightLine:
                    inSightOneDirection.add(treeInSightPoint)
                    treeInSightHeight = self.get(treeInSightPoint)
                    if treeInSightHeight >= treeCenterHeight:
                        break

                inSigth[direction] = inSightOneDirection

            scenicScore = prod((len(lane) for lane in inSigth.values()))
            allScenicScores[treeCenterPoint] = {
                "point": treeCenterPoint,
                "scenicScore": scenicScore,
                "inSight": inSigth,
            }
            # self.printVisibleTrees(visibleTrees=set.union(*inSigth.values()), centerTree=treeCenterPoint)

        return allScenicScores

    def printVisibleTrees(self, visibleTrees=None, centerTree=None):
        visibleTrees = visibleTrees or self.pointIterator
        print("")
        print("*" * len(self.map[0]))
        line = ""
        for point in self:
            if point in visibleTrees:
                line += str(self.get(point))
            elif centerTree and point == centerTree:
                line += "x"
            else:
                line += "."
            if len(line) == len(self.map[0]):
                print(line)
                line = ""
        print("*" * len(self.map[0]))
        print("")


def answer1(iterable):
    treeHeightMap = TreeHeightMap(iterable)
    return len(treeHeightMap.allVisibleTrees())


def answer2(iterable):
    treeHeightMap = TreeHeightMap(iterable)
    scores = treeHeightMap.allScenicScores()
    scoresByValues = sorted([score for score in scores.values()], key=lambda s: s["scenicScore"], reverse=True)
    print("Scenic score = %s" % scoresByValues[0]["scenicScore"])
    treeHeightMap.printVisibleTrees(
        visibleTrees=set.union(*scoresByValues[0]["inSight"].values()), centerTree=scoresByValues[0]["point"]
    )

    return scoresByValues[0]["scenicScore"]


# print(answer1(inputLines))
print(answer2(inputLines))
