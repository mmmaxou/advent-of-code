import os

inputPath = os.path.join(os.path.dirname(__file__), "input")

with open(inputPath, "r") as inputFile:
    lines = [line for line in inputFile.readlines() if line]


def answer1(inp):
    horizontal = 0
    depth = 0
    commands = {
        "forward": lambda x, horizontal, depth: [horizontal + x, depth],
        "down": lambda x, horizontal, depth: [horizontal, depth + x],
        "up": lambda x, horizontal, depth: [horizontal, depth - x]
    }
    for line in inp:
        command, value = line.split(" ")
        horizontal, depth = commands[command](int(value), horizontal, depth)

    return horizontal * depth


def answer2(inp):
    horizontal = 0
    depth = 0
    aim = 0
    commands = {
        "forward": lambda x, horizontal, depth, aim: [horizontal + x, depth + (aim * x), aim],
        "down": lambda x, horizontal, depth, aim: [horizontal, depth, aim + x],
        "up": lambda x, horizontal, depth, aim: [horizontal, depth, aim - x]
    }
    for line in inp:
        command, value = line.split(" ")
        horizontal, depth, aim = commands[command](int(value), horizontal, depth, aim)

    return horizontal * depth

print(answer1(lines))
print(answer2(lines))
