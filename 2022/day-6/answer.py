import os
from collections import Counter

with open(os.path.join(os.path.dirname(__file__), "input"), "r") as inputFile:
    lines = [line.replace("\n", "") for line in inputFile.readlines() if line]


def iterateWithWindow(iterable, windowSize=2):
    for i in range(len(iterable) - windowSize + 1):
        yield iterable[i: i + windowSize]


def answer(iterable, window):
    for index, sequence in enumerate(iterateWithWindow(iterable, window)):
        if Counter(sequence).most_common(1)[0][1] == 1:
            return index + window


print(answer(lines[0], 4))
print(answer(lines[0], 14))
