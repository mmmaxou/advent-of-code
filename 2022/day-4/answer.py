import os

inputPath = os.path.join(os.path.dirname(__file__), "input")

with open(inputPath, "r") as inputFile:
    lines = [line.replace("\n", "") for line in inputFile.readlines() if line]


def answer(iterable):
    supersets = []
    for line in iterable:
        assignments = []
        for sections in line.split(","):
            rangeStart, rangeEnd = [int(value, 10) for value in sections.split("-")]
            assignments.append(set(range(rangeStart, rangeEnd + 1)))

        if assignments[0].issubset(assignments[1]) or assignments[1].issubset(assignments[0]):
            supersets.append(assignments)

    return len(supersets)


def answer2(iterable):
    intersections = []
    for line in iterable:
        assignments = []
        for sections in line.split(","):
            rangeStart, rangeEnd = [int(value, 10) for value in sections.split("-")]
            assignments.append(set(range(rangeStart, rangeEnd + 1)))

        if set.intersection(*assignments):
            intersections.append(line)

    return len(intersections)


print(answer(lines))
print(answer2(lines))