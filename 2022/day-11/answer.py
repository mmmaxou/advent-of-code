from __future__ import annotations

import os
import sys

from math import prod
from dataclasses import dataclass, field
from typing import List, Callable

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils import Map, Point, iterateWithWindow

with open(os.path.join(os.path.dirname(__file__), "input"), "r") as inputFile:
    rawInput = inputFile.read()


MODULO_WORRY = 1


def manageWorryAnswer1(worry):
    return worry // 3


def manageWorryAnswer2(worry):
    return worry % MODULO_WORRY


class Monkey:
    def __init__(self, name, startingItems, operation, test) -> None:
        self.name: str = name
        self.items: List[int] = startingItems
        self.operation: Operation = operation
        self.test: Test = test
        self.totalInspections = 0
        self.manageWorry: Callable = None

    def round(self, monkeys: List[Monkey]):
        numberOfItems = len(self.items)
        self.totalInspections += numberOfItems
        for _ in range(numberOfItems):
            item = self.items.pop(0)

            # 1: change level of worry of item
            itemAfterOperation = self.operation.apply(item)

            # 2: Manage worry. Answer 1 is divise by 3. Answer 2 is modulo it.
            itemManageWorry = self.manageWorry(itemAfterOperation)

            # 3: test if divisible
            sendToMonkey = self.test.apply(itemManageWorry)

            # 4: send to monkey
            monkeys[sendToMonkey].items.append(itemManageWorry)

    def printItems(self):
        print(self.name + " " + ", ".join([str(i) for i in self.items]))


class Operation:
    @staticmethod
    def Parse(line):
        left, operand, right = line.replace("old", "{old}").split(" ")
        datas = left + "," + right
        functionOperand = {"+": sum, "*": prod}[operand]
        return Operation(datas, functionOperand)

    def __init__(self, datas, operand) -> None:
        self.datas: str = datas
        self.operand: Callable = operand

    def apply(self, item):
        datas = [int(i) for i in self.datas.format(old=str(item)).split(",")]
        return self.operand(datas)


class Test:
    def __init__(self, divisible, testTrue, testFalse) -> None:
        self.divisible = divisible
        self.testTrue = testTrue
        self.testFalse = testFalse

    def valid(self, number):
        return number % self.divisible == 0

    def apply(self, number):
        if self.valid(number):
            return self.testTrue
        else:
            return self.testFalse


class MonkeyFactory:
    def parseName(self, line):
        self.name = line.strip()

    def parseStarting(self, line):
        self.starting = [int(i) for i in line.split(": ")[-1].split(", ")]

    def parseOperation(self, line):
        self.operation = Operation.Parse(line.split("new = ")[-1])

    def parseTest(self, lines):
        testDivisible = int(lines[0].split(" ")[-1])
        testTrue = int(lines[1].split(" ")[-1])
        testFalse = int(lines[2].split(" ")[-1])
        self.test = Test(testDivisible, testTrue, testFalse)

    def create(self):
        return Monkey(self.name, self.starting, self.operation, self.test)


def parseInput(raw) -> List[Monkey]:
    monkeys = []
    blocks = raw.split("\n\n")
    for block in blocks:
        factory = MonkeyFactory()
        name, starting, operation, *test = [i.strip() for i in block.split("\n")]
        factory.parseName(name)
        factory.parseStarting(starting)
        factory.parseOperation(operation)
        factory.parseTest(test)
        monkey = factory.create()
        monkeys.append(monkey)

    return monkeys


def answer(raw, rounds, manageWorry):
    global MODULO_WORRY
    monkeys = parseInput(raw)

    for monkey in monkeys:
        MODULO_WORRY = MODULO_WORRY * monkey.test.divisible
        monkey.manageWorry = manageWorry

    for roundNumber in range(1, rounds + 1):
        print("Round %s" % roundNumber)
        for monkey in monkeys:
            monkey.round(monkeys)
        # for monkey in monkeys:
        #     monkey.printItems()

        if roundNumber == 1 or roundNumber == 20 or roundNumber % 1000 == 0:
            for monkey in monkeys:
                print("%s inspected items %s times" % (monkey.name, monkey.totalInspections))
            pass

    totalInspections = sorted([monkey.totalInspections for monkey in monkeys], reverse=True)

    return prod(totalInspections[:2])


# print(answer(rawInput, 20, manageWorry=manageWorryAnswer1))
print(answer(rawInput, 10000, manageWorry=manageWorryAnswer2))
