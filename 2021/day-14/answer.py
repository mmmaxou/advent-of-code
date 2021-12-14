from __future__ import annotations
import os
import math
from collections import Counter
from functools import reduce

with open(os.path.join(os.path.dirname(__file__), "input"), "r") as inputFile:
    inputString = [line.replace("\n", "") for line in inputFile.readlines()]
    polymerTemplate = inputString[0]
    pairInsertionRulesStr = inputString[2:]
    pairInsertionRules = {rule.split(" -> ")[0]: rule.split(" -> ")[1] for rule in pairInsertionRulesStr}


class Polymer:
    def __init__(self, chain) -> None:
        self.chain = chain

    def applyRules(self, processedChain, nextLetter) -> str:
        pair = processedChain[-1] + nextLetter
        newChain = pairInsertionRules.get(pair, "")
        return processedChain + newChain + nextLetter

    def polymerisation(self) -> Polymer:
        newChain = reduce(self.applyRules, self.chain[1:], self.chain[0])
        return Polymer(newChain)


class PolymerCounter:
    def __init__(self, chain) -> None:
        self.pairs = Counter()
        for i, _ in enumerate(chain[:-1]):
            pair = chain[i] + chain[i + 1]
            self.pairs.update([pair])

    def polymerisation(self) -> None:
        pairChanges = Counter()
        for rule, newLetter in pairInsertionRules.items():
            pairChanges[rule] -= self.pairs[rule]
            pairChanges[rule[0] + newLetter] += self.pairs[rule]
            pairChanges[newLetter + rule[1]] += self.pairs[rule]
        self.pairs = self.pairs + pairChanges

    def letters(self) -> Counter:
        letters = Counter()
        for pair, amount in self.pairs.items():
            letters[pair[0]] += amount
            letters[pair[1]] += amount
        for letter, amount in letters.items():
            letters[letter] = math.ceil(amount / 2)
        return letters


def answer1(steps):
    polymer = Polymer(polymerTemplate)
    for _ in range(steps):
        polymer = polymer.polymerisation()
    counter = Counter(polymer.chain)
    sortedCount = counter.most_common()
    return sortedCount[0][1] - sortedCount[-1][1]


def answer2(steps):
    polymer = PolymerCounter(polymerTemplate)
    for _ in range(steps):
        polymer.polymerisation()
    counter = polymer.letters()
    sortedCount = counter.most_common()
    return sortedCount[0][1] - sortedCount[-1][1]

print(answer1(10))
print(answer2(40))
