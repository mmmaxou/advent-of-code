import os
from typing import Set
from collections import defaultdict
import itertools
import copy

inputPath = os.path.join(os.path.dirname(__file__), "input")

with open(inputPath, "r") as inputFile:
    lines = [line.strip() for line in inputFile.readlines() if line.strip()]


def parseLines(lines):
    rules = {}
    passwords = []
    for line in lines:
        if ":" in line:
            key, commands = line.split(":")
            subrules = commands.strip().split("|")
            rule = [[n for n in subrule.split(" ") if n != ""] for subrule in subrules]
            rules[key] = rule

        elif line != "":
            passwords.append(line)
    return rules, passwords


allSubregexes = {}


def createRegexes(rules, index, currentRegex=None):
    if index in allSubregexes:
        return allSubregexes[index]

    rule = rules[index]
    if rule[0][0][0] == '"':
        allSubregexes[index] = [rule[0][0].replace('"', "")]
        return allSubregexes[index]

    regexes = []
    for subrule in rule:
        layer = [""]
        for num in subrule:
            if num == index:
                subregexes = ["__" + num + "__"]
            else:
                subregexes = createRegexes(rules, num)
            layer = [l + s for s in subregexes for l in layer]
        regexes.append(layer)
    regexes = [item for sublist in regexes for item in sublist]
    allSubregexes[index] = regexes
    return allSubregexes[index]


def ruleOrContent(rules, index):
    if index[0] == "a" or index[0] == "b":
        return [index]
    else:
        return createRegexes(rules, index)


def testRecursive(rules, regexSplit, possiblePasswords, once=False):
    valids = []
    for p in possiblePasswords:
        word = copy.deepcopy(p)
        valid = True

        if len(regexSplit) >= 2:
            begins = ruleOrContent(rules, regexSplit[0])
            ends = ruleOrContent(rules, regexSplit[-1])
            combines = itertools.product(begins, ends)
            for b, e in combines:
                if word.startswith(b) and word.endswith(e):
                    word = word[len(b) : -len(e)]
                    assert len(word) == len(p) - len(b) - len(e)
                    pass
        elif len(re)
            pass
    return valids


def solve1():
    rules, passwords = parseLines(lines)
    regexes = createRegexes(rules, "0")
    validPasswords = [p for p in passwords if p in regexes]
    return len(validPasswords)


def solve2():
    rules, passwords = parseLines(lines)
    rules["8"] = [["42"], ["42", "8"]]
    rules["11"] = [["42", "31"], ["42", "11", "31"]]
    regexes = createRegexes(rules, "0")
    recurRegexes, unrecurRegexes = [], []
    for r in regexes:
        if "__" in r:
            recurRegexes.append(r)
        else:
            unrecurRegexes.append(r)

    # Remove obvious valid passwords without recursion
    validUnrecurPasswords, invalidUnrecurPasswords = [], []
    for p in passwords:
        if p in unrecurRegexes:
            validUnrecurPasswords.append(p)
        else:
            invalidUnrecurPasswords.append(p)

    # Remove passwords based on fixed part of recursions
    invalidUnrecurPasswordsCopy = copy.deepcopy(invalidUnrecurPasswords)
    validRecurPasswords = set()
    for r in recurRegexes:
        split = r.split("__")
        valids = testRecursive(rules, split, invalidUnrecurPasswordsCopy)
        for v in valids:
            validRecurPasswords.add(v)
            invalidUnrecurPasswordsCopy.remove(v)

    return


# print(solve1())
print(solve2())
