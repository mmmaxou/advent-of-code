import os
from collections import defaultdict
from parse import compile

inputPath = os.path.join(os.path.dirname(__file__), "input")

with open(inputPath, "r") as inputFile:
    lines = [line.strip() for line in inputFile.readlines() if bool(line)]

bagParser = compile("{amount:d} {}")


def parseRules(lines):
    contains = defaultdict(dict)
    containedBy = defaultdict(dict)

    def parseBag(bag, inputColor):
        parsed = bagParser.parse(bag)
        amount = parsed["amount"]
        outputColor = parsed[0]
        contains[inputColor][outputColor] = amount
        containedBy[outputColor][inputColor] = amount

    for line in lines:
        if line:
            line = line.replace(".", "").replace(" bags", " bag").replace(" bag", "")
            inputColor, end = line.split(" contain ")
            if end == "no other":
                contains[inputColor] = {}
            elif "," in end:
                for bag in end.split(","):
                    parseBag(bag, inputColor)
            else:
                parseBag(end, inputColor)

    return dict(contains), dict(containedBy)


def containedByRecursive(containedByCollection, color, canContain=set()):
    if color not in containedByCollection:
        return set()
    else:
        container = containedByCollection[color]
        for containerColor in container:
            canContain.add(containerColor)
            canContain.update(containedByRecursive(containedByCollection, containerColor))
        return canContain


def containsRecursive(containsCollection, color):
    if color not in containsCollection:
        return 0
    else:
        total = 0
        container = containsCollection[color]
        for containedColor in container:
            total += container[containedColor]
            total += container[containedColor] * containsRecursive(containsCollection, containedColor)
        return total


def solve(color):
    contains, containedBy = parseRules(lines)
    shinyGold = containedByRecursive(containedBy, color)
    return len(shinyGold)


def solve2(color):
    contains, containedBy = parseRules(lines)
    shinyGold = containsRecursive(contains, color)
    return shinyGold


print(solve("shiny gold"))
print(solve2("shiny gold"))
