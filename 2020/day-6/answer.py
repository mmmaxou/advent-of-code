import os
from collections import Counter

REQUIRED_FIELDS = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]
VALID_COLORS = "amb blu brn gry grn hzl oth".split(" ")

inputPath = os.path.join(os.path.dirname(__file__), "input")

with open(inputPath, "r") as inputFile:
    lines = [line.strip() for line in inputFile.readlines() if line]
    block = "\n".join(lines)


def parseLines(lines):
    groups = []
    batch = []
    for line in lines:
        if line == "":
            groups.append(batch)
            batch = []
        else:
            for field in list(line):
                batch.append(field)
    return groups


def parseLines2(block):
    return [group.split("\n") for group in block.split("\n\n")]


def solve():
    groups = parseLines(lines)
    counts = [len(Counter(group)) for group in groups]
    total = sum(counts)
    return total


def solve2():
    groups = parseLines2(block)
    everyones = []
    for group in groups:
        counter = Counter()
        for line in group:
            counter.update(list(line))
        everyone = [key for key in counter if counter[key] == len(group)]
        everyones.append(everyone)

    counts = [len(everyone) for everyone in everyones]
    total = sum(counts)
    return total


print(solve())
print(solve2())
