import os

inputPath = os.path.join(os.path.dirname(__file__), "input")

with open(inputPath, "r") as inputFile:
    lines = [int(line) for line in inputFile.readlines() if line]


def answer(iterable, slidingWindow):
    count = 0
    for i in range(1, len(iterable) - slidingWindow + 1):
        current = sum(iterable[i: i + slidingWindow])
        before = sum(iterable[i - 1: i - 1 + slidingWindow])
        if current > before:
            count += 1
    return count


print(answer(lines, 1))
print(answer(lines, 3))
