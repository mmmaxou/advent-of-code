import os

from collections import deque

inputPath = os.path.join(os.path.dirname(__file__), "input")

with open(inputPath, "r") as inputFile:
    lines = [line.replace("\n", "") for line in inputFile.readlines() if line]


def parseCargo(iterable):
    # Find the line with cargo pile numbers
    cargoLine = 0
    pilesAmount = 0
    for index, line in enumerate(iterable):
        try:
            [int(i, 10) for i in line.split(" ") if i]
        except ValueError:
            continue
        cargoLine = index - 1
        pilesAmount = [int(i, 10) for i in line.split(" ") if i][-1]
        break

    # Iterate in reverse order to find stack the piles
    piles = [deque() for i in range(pilesAmount)]
    pilesIndexes = [i * 4 + 1 for i in range(pilesAmount)]
    for line in iterable[cargoLine:: -1]:
        for cargoIndex, pileIndex in enumerate(pilesIndexes):
            crate = line[pileIndex]
            if crate != " ":
                piles[cargoIndex].append(crate)

    return piles, cargoLine


def crateMover9000(piles, instructions):
    for line in instructions:
        _, amount, _, src, _, dst = line.split(" ")
        for _ in range(int(amount)):
            crate = piles[int(src) - 1].pop()
            piles[int(dst) - 1].append(crate)


def crateMover9001(piles, instructions):
    for line in instructions:
        _, amount, _, src, _, dst = line.split(" ")
        tempCrate = deque()

        for _ in range(int(amount)):
            crate = piles[int(src) - 1].pop()
            tempCrate.append(crate)

        for _ in range(int(amount)):
            crate = tempCrate.pop()
            piles[int(dst) - 1].append(crate)


def answer(iterable, mover):
    piles, cargoLine = parseCargo(iterable)
    mover(piles, iterable[cargoLine + 3:])
    message = "".join(pile[-1] for pile in piles)
    return message


print(answer(lines, crateMover9000))
print(answer(lines, crateMover9001))
