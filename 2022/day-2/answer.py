import os

inputPath = os.path.join(os.path.dirname(__file__), "input")

with open(inputPath, "r") as inputFile:
    lines = [line.replace("\n", "") for line in inputFile.readlines() if line]


WIN = ["C X", "A Y", "B Z"]
TIE = ["A X", "B Y", "C Z"]
LOST = ["B X", "C Y", "A Z"]
SCORE = {"A": 1, "B": 2, "C": 3, "X": 1, "Y": 2, "Z": 3}
STRATEGY = {"X": [LOST, 0], "Y": [TIE, 3], "Z": [WIN, 6]}


def computeScore(line):
    opponent, me = line.split(" ")
    score = SCORE[me]
    outcome = 6 * int(line in WIN) + 3 * int(line in TIE) + 0 * int(line in LOST)
    return score + outcome


def computeScore2(line):
    opponent, strategyChoice = line.split(" ")
    pairs, outcome = STRATEGY[strategyChoice]
    whatToPlay = next(iter(pair for pair in pairs if opponent in pair))
    opponent, me = whatToPlay.split(" ")
    score = SCORE[me]
    return score + outcome


def answer(iterable):
    scores = [computeScore(line) for line in iterable]
    return sum(scores)


def answer2(iterable):
    scores = [computeScore2(line) for line in iterable]
    return sum(scores)

print(answer(lines))
print(answer2(lines))
