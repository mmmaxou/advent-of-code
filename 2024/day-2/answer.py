import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from utils import iterateWithWindow

inputPath = os.path.join(os.path.dirname(__file__), "input")

with open(inputPath, "r") as inputFile:
    raw = [line.strip() for line in inputFile.readlines()]


def pairwise(iterable):
    """s -> (s0,s1), (s1,s2), (s2, s3), ..."""
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def answer(iterable, maxProblemDampener):

    total = 0
    for lineIndex, line in enumerate(iterable):
        datasToTry = [[int(val) for val in line.split(" ")]]
        safe = False
        cpt = 0
        dampener = 0
        while datasToTry and cpt < 100:
            cpt += 1
            data = datasToTry.pop()
            error = False
            increasing = True
            decreasing = True
            gap = True
            for index, beforeAndcurrent in enumerate(
                iterateWithWindow(data, windowSize=2)
            ):
                before, current = beforeAndcurrent
                increasing = increasing and before < current
                decreasing = decreasing and before > current
                gap = gap and abs(before - current) <= 3 and abs(before - current) >= 1
                error = not (gap and (increasing or decreasing))
                if error:
                    if dampener < maxProblemDampener:
                        dampener += 1
                        datasToTry.append(data[: index + 1] + data[index + 2 :])
                        datasToTry.append(data[:index] + data[index + 1 :])
                        datasToTry.append(data[1:])
                    break

            if not error:
                safe = True

        print(
            "[%s] line '%s' is %s"
            % (lineIndex, line, "safe" if safe else "not safe at all")
        )
        # input("Check ? ")
        total += int(safe)

    return total


# print(answer(raw, maxProblemDampener=0))
print(answer(raw, maxProblemDampener=1))
# print(answer(raw))
