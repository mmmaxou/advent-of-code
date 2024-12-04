import os
import re
import functools

inputPath = os.path.join(os.path.dirname(__file__), "input")

with open(inputPath, "r") as inputFile:
    raw = inputFile.read().replace("\n", "")


def answer(iterable):
    regex = re.compile(r"mul\((\d{1,3})\,(\d{1,3})\)")
    values = regex.findall(iterable)
    res = functools.reduce(lambda x, y: x + int(y[0]) * int(y[1]), values, 0)
    return res


def answer_bis(iterable):
    betweenDoAndDonts = re.compile(r"do\(\)(.*?)don't\(\)")
    regex = re.compile(r"mul\((\d{1,3})\,(\d{1,3})\)")
    values = betweenDoAndDonts.findall("do()" + iterable + "don't()")
    allMuls = []
    for value in values:
        allMuls += regex.findall(value)
    res = functools.reduce(lambda x, y: x + int(y[0]) * int(y[1]), allMuls, 0)
    return res


print(answer(raw))
print(answer_bis(raw))
