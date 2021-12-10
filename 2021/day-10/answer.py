import os

with open(os.path.join(os.path.dirname(__file__), "input"), "r") as inputFile:
    inputString = [line.replace("\n", "") for line in inputFile.readlines()]

OPEN = {"[": "]", "(": ")", "{": "}", "<": ">"}
CLOSE = {value: key for key, value in OPEN.items()}
VALUES = {")": 3, "]": 57, "}": 1197, ">": 25137}
AUTOCOMPLETE_VALUE = {")": 1, "]": 2, "}": 3, ">": 4}


def answer1(lines):
    illegalCharacters = []
    for line in lines:
        unresolved = []
        for char in line:
            if char in OPEN:
                unresolved.append(char)
            elif char in CLOSE:
                if CLOSE[char] == unresolved[-1]:
                    unresolved.pop(len(unresolved) - 1)
                else:
                    illegalCharacters.append(char)
                    break
    sumIllegals = sum(VALUES[char] for char in illegalCharacters)
    return sumIllegals


def answer2(lines):
    incompletes = []
    for line in lines:
        unresolved = []
        for char in line:
            if char in OPEN:
                unresolved.append(char)
            elif char in CLOSE:
                if CLOSE[char] == unresolved[-1]:
                    unresolved.pop(len(unresolved) - 1)
                else:
                    break
        else:
            incompletes.append(unresolved)

    completions = []
    for incomplete in incompletes:
        completion = [OPEN[char] for char in incomplete[::-1]]
        completions.append(completion)

    scores = []
    for completion in completions:
        score = 0
        for char in completion:
            score *= 5
            score += AUTOCOMPLETE_VALUE[char]
        scores.append(score)

    scores.sort()
    middleScore = scores[int((len(scores) - 1) / 2)]
    return middleScore

print(answer1(inputString))
print(answer2(inputString))
