import os
import copy
from typing import Deque, List
from collections import deque

inputPath = os.path.join(os.path.dirname(__file__), "input")

with open(inputPath, "r") as inputFile:
    charsList = [line.strip().replace(" ", "") for line in inputFile.readlines() if line.strip()]


class Node:
    def resolve(self) -> int:
        raise NotImplementedError()


class Operator(Node):
    CHARS = ["+", "*"]

    @staticmethod
    def FromChar(char: str):
        if char == "+":
            return Add()
        elif char == "*":
            return Multiply()

    def resolve(self, n1: Node, n2: Node) -> int:
        raise NotImplementedError()


class Add(Operator):
    def __repr__(self) -> str:
        return "+"

    def resolve(self, n1: Node, n2: Node) -> int:
        return n1.resolve() + n2.resolve()


class Multiply(Operator):
    def __repr__(self) -> str:
        return "*"

    def resolve(self, n1: Node, n2: Node) -> int:
        return n1.resolve() * n2.resolve()


class Number(Node):
    def __init__(self, value) -> None:
        self.value = int(value)
        self.valueStr = str(value)

    def resolve(self) -> int:
        return self.value

    def __repr__(self) -> str:
        return self.valueStr


class Operation(Node):
    PRIORITY_OPEN = "("
    PRIORITY_CLOSE = ")"

    @classmethod
    def FromLine(cls, chars: Deque[str]):
        nodes: List[Node] = []
        while chars:
            char = chars.popleft()
            if char in Operator.CHARS:
                operator = Operator.FromChar(char)
                nodes.append(operator)
            elif char in cls.PRIORITY_OPEN:
                operation = cls.FromLine(chars)
                nodes.append(operation)
            elif char in cls.PRIORITY_CLOSE:
                return cls(nodes)
            else:
                assert int(char)
                nodes.append(Number(char))
        return cls(nodes)

    def __init__(self, nodes: List[Node]) -> None:
        self.nodes = nodes

    def resolve(self, nodes=None) -> int:
        nodes = nodes or deque(copy.deepcopy(self.nodes))
        while len(nodes) >= 3:
            n1 = nodes.popleft()
            op = nodes.popleft()
            n2 = nodes.popleft()
            assert isinstance(op, Operator)
            res = Number(op.resolve(n1, n2))
            nodes.appendleft(res)
        assert len(nodes) == 1
        return nodes[0].resolve()

    def __repr__(self) -> str:
        return "(%s)" % (" ".join([repr(n) for n in self.nodes]))


class OperationAdditionPredecede(Operation):
    def resolve(self, nodes=None) -> int:
        nodes = nodes or deque(copy.deepcopy(self.nodes))
        rotation = 0
        while len(nodes) >= 3:
            if rotation + 1 >= len(nodes):
                nodes.rotate(rotation)
                break
            if isinstance(nodes[1], Multiply):
                rotation += 2
                nodes.rotate(-2)
            else:
                n1 = nodes.popleft()
                op = nodes.popleft()
                n2 = nodes.popleft()
                assert isinstance(op, Add)
                res = Number(op.resolve(n1, n2))
                nodes.appendleft(res)
                nodes.rotate(rotation)
                rotation = 0

        for node in nodes:
            if isinstance(node, Operator):
                assert isinstance(node, Multiply)

        return super(OperationAdditionPredecede, self).resolve(nodes)


def getDequeFromChars(chars):
    return deque(copy.deepcopy(chars))


def solve1():
    sums = []
    for chars in charsList:
        copyList = getDequeFromChars(chars)
        operation = Operation.FromLine(copyList)
        res = operation.resolve()
        print("%s = %s" % (chars, res))
        sums.append(res)
    return sum(sums)


def solve2():
    sums = []
    for chars in charsList:
        copyList = getDequeFromChars(chars)
        operation = OperationAdditionPredecede.FromLine(copyList)
        res = operation.resolve()
        print("%s = %s" % (chars, res))
        sums.append(res)
    return sum(sums)


# print(solve1())
print(solve2())
