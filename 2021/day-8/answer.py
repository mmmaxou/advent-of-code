import os

with open(os.path.join(os.path.dirname(__file__), "input"), "r") as inputFile:
    inputString = [line for line in inputFile.readlines()]


UNIQUE_NUMBER_OF_SEGMENTS = set([2, 3, 4, 7])


def parseLine(line):
    return [part.split() for part in line.split(" | ")]


def hasUniqueNumberOfSegment(pattern):
    return len(pattern) in UNIQUE_NUMBER_OF_SEGMENTS


def containsSegment(container, contained):
    return all([letter in container for letter in contained])


def getCorrespondance(correspondance, inSegments):
    for i, segments in enumerate(correspondance):
        if segments == set(inSegments):
            return i


def carefulAnalysis(signals):
    signals = list(map(set, signals))

    # Obvious unique solutions
    n1 = next(iter(p for p in signals if len(p) == 2))
    n4 = next(iter(p for p in signals if len(p) == 4))
    n7 = next(iter(p for p in signals if len(p) == 3))
    n8 = next(iter(p for p in signals if len(p) == 7))

    # Segments:

    #  aaaa
    # b    c
    # b    c
    #  dddd
    # e    f
    # e    f
    #  gggg

    # n3 contains (cf) and has 5 segments
    cf = n1
    n3 = next(iter(signal for signal in signals if len(signal) == 5 and containsSegment(signal, cf)))

    # Figure out the segments (be)
    be = n8.difference(n3)

    # Figure out n0 has it is the only unknown signal with segments be & cf
    knownSignals = [n1, n3, n4, n7, n8]
    unknownSignals = [signal for signal in signals if signal not in knownSignals]
    n0 = next(iter(signal for signal in unknownSignals if containsSegment(signal, be) and containsSegment(signal, cf)))

    # Figure out n6 has it is the only unknown signal with segments be
    knownSignals = [n0, n1, n3, n4, n7, n8]
    unknownSignals = [signal for signal in signals if signal not in knownSignals]
    n6 = next(iter(signal for signal in unknownSignals if containsSegment(signal, be)))

    # Figure out n9 has it is the only unknown signal with segments cf
    knownSignals = [n0, n1, n3, n4, n6, n7, n8]
    unknownSignals = [signal for signal in signals if signal not in knownSignals]
    n9 = next(iter(signal for signal in unknownSignals if containsSegment(signal, cf)))

    # Figure out segment c and f
    c = n8.difference(n6)
    f = n1.difference(c)

    # Figure out n2 and n5
    knownSignals = [n0, n1, n3, n4, n6, n7, n8, n9]
    unknownSignals = [signal for signal in signals if signal not in knownSignals]
    n2 = next(iter(signal for signal in unknownSignals if containsSegment(signal, c)))
    n5 = next(iter(signal for signal in unknownSignals if containsSegment(signal, f)))

    correspondance = [n0, n1, n2, n3, n4, n5, n6, n7, n8, n9]

    return correspondance


def answer1(lines):
    allUniquePatterns = []
    for line in lines:
        signalPatterns, outputValue = parseLine(line)
        uniquePatterns = [p for p in outputValue if hasUniqueNumberOfSegment(p)]
        allUniquePatterns.extend(uniquePatterns)
    return len(allUniquePatterns)


def answer2(lines):
    lineValues = []
    for line in lines:
        signalPatterns, outputValue = parseLine(line)
        correspondance = carefulAnalysis(signalPatterns)
        outputNumbers = [getCorrespondance(correspondance, segments) for segments in outputValue]
        total = int("".join(map(str, outputNumbers)), 10)
        lineValues.append(total)
    return sum(lineValues)


print(answer1(inputString))
print(answer2(inputString))
