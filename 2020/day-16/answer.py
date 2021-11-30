import os
from parse import compile
from typing import List
from collections import defaultdict
import copy

inputPath = os.path.join(os.path.dirname(__file__), "input")


class Range:
    def __init__(self, start, end) -> None:
        self.start: int = start
        self.end: int = end

    def isInside(self, value) -> bool:
        return value >= self.start and value <= self.end

    def __str__(self) -> str:
        return "%s-%s" % (self.start, self.end)

    __repr__ = __str__


class Field:

    FieldParse = compile("{name}: {start1:d}-{end1:d} or {start2:d}-{end2:d}")

    @staticmethod
    def From(lineStr):
        parsing = Field.FieldParse.parse(lineStr).named
        return Field(
            parsing["name"], [Range(parsing["start1"], parsing["end1"]), Range(parsing["start2"], parsing["end2"])]
        )

    def __init__(self, name, ranges) -> None:
        self.name: str = name
        self.ranges: List[Range] = ranges

    def isInside(self, value) -> bool:
        return any(r.isInside(value) for r in self.ranges)

    def __str__(self) -> str:
        return "%s: %s" % (self.name, " or ".join(map(str, self.ranges)))

    __repr__ = __str__


def solve1(fields: List[Field], nearbyTickets: List[List[int]]):
    invalids = []
    for ticket in nearbyTickets:
        for value in ticket:
            if not any(field.isInside(value) for field in fields):
                invalids.append(value)
    return sum(invalids)


def solve2(fields: List[Field], nearbyTickets: List[List[int]], myTicket: List[int]):
    validTickets = []

    # Get valid tickets
    for ticket in nearbyTickets:
        ticketValid = True
        for value in ticket:
            if not any(field.isInside(value) for field in fields):
                ticketValid = False
        if ticketValid:
            validTickets.append(ticket)

    # Try to determine fields
    ticketLen = len(myTicket)
    possiblePositionsByField = defaultdict(list)
    for field in fields:
        for i in range(ticketLen):
            values = [ticket[i] for ticket in validTickets]
            insides = [field.isInside(value) for value in values]
            possibleField = all(insides)
            if possibleField:
                possiblePositionsByField[field.name].append(i)

    validFieldByPosition = {}
    possiblePositionsByFieldCopy = dict(copy.deepcopy(possiblePositionsByField))
    cpt = 0
    while possiblePositionsByFieldCopy:
        cpt += 1
        toDelete = []
        for field, positions in possiblePositionsByFieldCopy.items():
            filteredPositions = [p for p in positions if p not in validFieldByPosition]
            if len(filteredPositions) == 1:
                toDelete.append(field)
                validFieldByPosition[filteredPositions[0]] = field
                break

        assert len(toDelete) == 1
        for field in toDelete:
            del possiblePositionsByFieldCopy[field]

    # Get the departure positions
    prod = 1
    for index, value in enumerate(myTicket):
        field = validFieldByPosition[index]
        if field.startswith("departure"):
            prod = prod * value

    return prod


with open(inputPath, "r") as inputFile:
    lines = [line.strip() for line in inputFile.readlines() if line]
    block = "\n".join(lines)
    groups = block.split("\n\n")
    fieldsStr, myTicketStr, nearbyTicketStr = groups
    fields = [Field.From(line) for line in fieldsStr.split("\n")]
    myTicket = [int(number) for line in myTicketStr.split("\n")[1:] for number in line.split(",")]
    nearbyTickets = [[int(number) for number in line.split(",")] for line in nearbyTicketStr.split("\n")[1:]]


# print(solve1(fields, nearbyTickets))
print(solve2(fields, nearbyTickets, myTicket))
