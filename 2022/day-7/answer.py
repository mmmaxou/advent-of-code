from __future__ import annotations
from dataclasses import dataclass, field

import os
from typing import List, OrderedDict

with open(os.path.join(os.path.dirname(__file__), "input"), "r") as inputFile:
    blocks = [[l for l in line.split("\n") if l] for line in inputFile.read().split("$ ") if line]


@dataclass
class Node:
    name: str = ""
    parent: Node = None
    children: OrderedDict[str, Node] = field(default_factory=lambda: OrderedDict())

    def __post_init__(self):
        if self.parent:
            self.parent.addChild(self)

    def addChild(self, child: Node):
        self.children[child.name] = child

    def visit(self, visitor, *args, **kwargs):
        visitor(self, *args, **kwargs)
        return {"args": args, "kwargs": kwargs}

    def print(self):
        raise NotImplementedError()

    def getSize(self):
        raise NotImplementedError()


@dataclass
class Folder(Node):
    def cd(self, arg):
        res = {
            "/": self if self.parent is self else self.parent.cd("/"),
            "..": self.parent,
        }
        return res.get(arg, None) or self.children[arg]

    def ls(self, childs: List[str]):
        for child in childs:
            commandOrSize, name = child.split(" ")
            if commandOrSize == "dir":
                self.addChild(Folder(name=name, parent=self))
            else:
                self.addChild(File(name=name, size=int(commandOrSize, 10), parent=self))

    def visit(self, visitor, *args, **kwargs):
        visitor(self, *args, **kwargs)
        for child in self.children.values():
            child.visit(visitor, *args, **kwargs)
        return {"args": args, "kwargs": kwargs}

    def print(self, space=""):
        print("%s- %s (dir)" % (space, self.name))
        for child in self.children.values():
            child.print(space + "  ")

    def getSize(self):
        if not hasattr(self, "size"):
            self.size = sum([child.getSize() for child in self.children.values()])
        return self.size


@dataclass
class Root(Folder):
    def __post_init__(self):
        self.parent = self
        self.name = "/"


@dataclass
class File(Node):
    size: int = 0

    def getSize(self):
        return self.size

    def addChild(self, child: Node):
        raise Exception("Can't add a child to a File")

    def print(self, space):
        print("%s- %s (file, size=%s)" % (space, self.name, self.size))


class Parser:
    def __init__(self):
        self.root = Root()
        self.cwd = self.root

    def parse(self, blocks):
        for block in blocks:
            self._parseBlock(block)
        return self

    def _parseBlock(self, block: List[str]):
        if block[0].startswith("cd"):
            self.cwd = self.cwd.cd(block[0].split(" ")[-1])
        elif block[0].startswith("ls"):
            self.cwd.ls(block[1:])
        else:
            raise Exception("Unknown command %s" % block[0])


def atMost(node, value=0, allNodes=[]):
    size = node.getSize()
    if isinstance(node, Folder) and size < value:
        allNodes.append(size)


def atLeast(node, value=0, allNodes=[]):
    size = node.getSize()
    if isinstance(node, Folder) and size >= value:
        allNodes.append(size)


def include(node, allNodes=[]):
    allNodes.append(node.getSize())


def answer1(iterable):
    allNodes = Parser().parse(iterable).root.visit(atMost, value=100000, allNodes=[])["kwargs"]["allNodes"]
    return sum(allNodes)


def answer2(iterable):
    allNodes = Parser().parse(iterable).root.visit(include, allNodes=[])["kwargs"]["allNodes"]
    requiredSpace = 30000000 - (70000000 - max(allNodes))
    allNodes = Parser().parse(iterable).root.visit(atLeast, value=requiredSpace, allNodes=[])["kwargs"]["allNodes"]
    return min(allNodes)


print(answer1(blocks))
print(answer2(blocks))
