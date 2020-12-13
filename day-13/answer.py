import os
import operator
from functools import reduce

inputPath = os.path.join(os.path.dirname(__file__), "input")

with open(inputPath, "r") as inputFile:
    initialLines = [line.strip() for line in inputFile.readlines() if line.strip()]
    departureTimestamp = int(initialLines[0])
    IDs = [int(n) if n != "x" else n for n in initialLines[1].split(",")]


def solve1():
    cpt = 0
    while cpt < 100:
        for id in IDs:
            if id != "x":
                if (departureTimestamp + cpt) % id == 0:
                    return id * cpt
        cpt += 1


def nextMultiplier(timestamp, pointers):
    for index, pointer in enumerate(pointers):
        id = IDs[pointer]
        if (timestamp + pointer) % id != 0:
            return pointers[index-1]


def prod(iterable):
    return reduce(operator.mul, iterable, 1)


def solve2():
    pointers = [index for index, id in enumerate(IDs) if id != "x"]
    accumulator = [prod([n if n != "x" else 1 for n in IDs[0: i+1]]) for i in range(len(IDs))]
    timestamp = IDs[pointers[0]]
    while True:
        pointer = nextMultiplier(timestamp, pointers)
        if pointer is None:
            return timestamp
        else:
            timestamp += accumulator[pointer]


# print(solve1())
print(solve2())
