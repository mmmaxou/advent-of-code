import os
from collections import Counter
from typing import Dict
from zlib import crc32

with open(os.path.join(os.path.dirname(__file__), "input"), "r") as inputFile:
    inputString = [line.replace("\n", "") for line in inputFile.readlines()]


def bytes_to_float(b):
    return float(crc32(b) & 0xffffffff) / 2**32

class Node:
    def __init__(self, name) -> None:
        self.name = name
        self.connections = set()

    def addConnection(self, other):
        self.connections.add(other)
        other.connections.add(self)


class Cave:
    def __init__(self, node: Node, medium=False) -> None:
        self.node = node
        if medium:
            self.small = node.name in ["start", "end"]
            self.medium = not node.name.isupper() and not self.small
        else:
            self.small = not node.name.isupper()
            self.medium = False


class Path:
    def __init__(self, elements=None) -> None:
        self.list = elements or []
        self.counter = Counter()
        self.smallVisitedTwice = None
        self.repr = ""

    def __iter__(self):
        return iter(self.list)

    def copyAndAppend(self, cave):
        newPath = Path()
        newPath.list = self.list.copy()
        newPath.list.append(cave)
        newPath.smallVisitedTwice = self.smallVisitedTwice
        newPath.counter = Counter(self.counter)
        newPath.counter[cave.node.name] += 1
        newPath.repr = ",".join([cave.node.name for cave in self])
        if not newPath.smallVisitedTwice:
            for key, amount in newPath.counter.items():
                if key not in ["start", "end"] and not key.isupper() and amount == 2:
                    newPath.smallVisitedTwice = key
        return newPath

    def isValid(self, otherPaths):
        lastCave = self.list[-1]
        visited = self.counter[lastCave.node.name] - 1
        if lastCave.small and visited == 1:
            return False
        if lastCave.medium:
            if self.smallVisitedTwice == lastCave.node.name:
                if visited == 2:
                    return False
            else:
                if visited == 1:
                    return False
        if self in otherPaths:
            return False
        return True

    def __eq__(self, __o: object) -> bool:
        if len(self.list) != len(__o.list):
            return False
        for i, cave in enumerate(self.list):
            if cave != __o.list[i]:
                return False
        return True

    def __hash__(self) -> int:
        return hash(repr(self))

    def __repr__(self) -> str:
        return self.repr

class Labyrinth:
    def __init__(self, medium=False) -> None:
        self.paths = set()
        self.medium = medium

    def start(self, node):
        cave = Cave(node, self.medium)
        startPath = Path().copyAndAppend(cave)
        self.paths.add(startPath)
        self.traverse(startPath)
    
    def traverse(self, path: Path):
        if path.list[-1].node.name == "end":
            return
        newPaths = []
        for node in path.list[-1].node.connections:
            newCave = Cave(node, self.medium)
            newPath = path.copyAndAppend(newCave)
            if newPath.isValid(self.paths):
                newPaths.append(newPath)
        try:
            self.paths.remove(path)
        except ValueError:
            pass
        self.paths.update(newPaths)
        for newPath in newPaths:
            self.traverse(newPath)


def createNodes(lines):
    nodes = {name: Node(name) for name in set(("-".join(lines)).split("-"))}
    createConnections(nodes, lines)
    return nodes


def createConnections(nodes: Dict[str, Node], lines):
    for line in lines:
        a, b = line.split("-")
        nodes[a].addConnection(nodes[b])
        

def answer1(lines):
    nodes = createNodes(lines)
    labyrinth = Labyrinth()
    labyrinth.start(nodes["start"])
    return len(labyrinth.paths)


def answer2(lines):
    nodes = createNodes(lines)
    labyrinth = Labyrinth(medium=True)
    labyrinth.start(nodes["start"])
    return len(labyrinth.paths)

print(answer1(inputString))
print(answer2(inputString))
