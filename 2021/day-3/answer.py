import os
import collections

inputPath = os.path.join(os.path.dirname(__file__), "input")

with open(inputPath, "r") as inputFile:
    lines = [line.replace("\n", "") for line in inputFile.readlines() if line]


def transpose(matrix):
    rows = []
    for line in matrix:
        for index, bit in enumerate(line):
            if len(rows) == index:
                rows.append([])
            rows[index].append(bit)
    return rows


def answer1(inp):
    transposedInput = transpose(inp)

    # Get epsilon and gamma
    epsilonBit = ""
    gammaBit = ""
    for row in transposedInput:
        count = collections.Counter(row)
        epsilonBit += str(int(count["0"] >= count["1"]))
        gammaBit += str(int(count["0"] < count["1"]))

    epsilon = int(epsilonBit, 2)
    gamma = int(gammaBit, 2)

    return epsilon * gamma


def filterRating(inp, index, bitCriteria):
    if len(inp) == 1:
        return inp

    transposedInput = transpose(inp)
    row = transposedInput[index]
    count = collections.Counter(row)
    if (bitCriteria == "mostCommon" and count["1"] >= count["0"]) or (
        bitCriteria == "leastCommon" and count["1"] < count["0"]
    ):
        filteredInput = [line for line in inp if line[index] == "1"]
    else:
        filteredInput = [line for line in inp if line[index] == "0"]

    nextFilteredInput = filterRating(filteredInput, index + 1, bitCriteria)
    return nextFilteredInput


def answer2(inp):
    oxygenGeneratorBit = filterRating(inp, 0, "mostCommon")[0]
    CO2ScrubberBit = filterRating(inp, 0, "leastCommon")[0]

    oxygenGenerator = int(oxygenGeneratorBit, 2)
    CO2Scrubber = int(CO2ScrubberBit, 2)

    return oxygenGenerator * CO2Scrubber


print(answer1(lines))
print(answer2(lines))
