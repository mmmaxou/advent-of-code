import os

inputPath = os.path.join(os.path.dirname(__file__), "input")

with open(inputPath, "r") as inputFile:
    initialLines = [line.strip() for line in inputFile.readlines() if line]


def getLineAtCursor(lines, cursor):
    command, value = lines[cursor].split(" ")
    value = int(value)
    return command, value


def advance(lines, cursor, accumulator):
    command, value = getLineAtCursor(lines, cursor)
    if command == "acc":
        accumulator += value
        cursor += 1
    elif command == "jmp":
        cursor += value
    elif command == "nop":
        cursor += 1
    else:
        raise Exception("Wtf")
    return cursor, accumulator


def stopAtLoop(lines, cursor, accumulator, alreadyVisited):
    if cursor >= len(initialLines):
        return accumulator, True
    if cursor in alreadyVisited:
        return accumulator, False
    else:
        alreadyVisited.add(cursor)
        cursor, accumulator = advance(lines, cursor, accumulator)
        return stopAtLoop(lines, cursor, accumulator, alreadyVisited)


def invertLine(line):
    if line.startswith("nop"):
        return line.replace("nop", "jmp")
    elif line.startswith("jmp"):
        return line.replace("jmp", "nop")
    else:
        raise Exception("Wtf")


def resolveLoop(lines):
    copyLines = lines.copy()
    for i in range(len(lines)):
        if not lines[i].startswith("acc"):
            invertedLine = invertLine(lines[i])
            copyLines[i] = invertedLine
            accumulator, terminated = stopAtLoop(copyLines, 0, 0, set())
            if terminated:
                return accumulator
            else:
                copyLines[i] = lines[i]


def solve1():
    return stopAtLoop(initialLines, 0, 0, set())


def solve2():
    return resolveLoop(initialLines)


print(solve1())
print(solve2())
