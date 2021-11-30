import os
from functools import reduce
from itertools import combinations
from collections import Counter

inputPath = os.path.join(os.path.dirname(__file__), "input")

with open(inputPath, "r") as inputFile:
    lines = [line.strip() for line in inputFile.readlines() if line]


def firstPolicy(password, letter, occurenceMin, occurenceMax):
    counter = Counter(password)
    return counter[letter] <= occurenceMax and counter[letter] >= occurenceMin


def secondPolicy(password, letter, occurenceMin, occurenceMax):
    occurences = [occurenceMin, occurenceMax]
    validOccurences = [password[occ - 1] == letter for occ in occurences]
    return xorIterable(validOccurences)


def xorIterable(iterable):
    return reduce(lambda a, b: a ^ b, iterable)


def isValidPassword(line: str, policy):
    occurences, letter, password = line.split(" ")
    occurenceMin, occurenceMax = map(int, occurences.split("-"))
    letter = letter[0]

    return policy(password, letter, occurenceMin, occurenceMax)


validPasswordsFirstPolicy = [p for p in lines if isValidPassword(p, firstPolicy)]
validPasswordsSecondPolicy = [p for p in lines if isValidPassword(p, secondPolicy)]

print(len(validPasswordsFirstPolicy))
print(len(validPasswordsSecondPolicy))

print("cc")
