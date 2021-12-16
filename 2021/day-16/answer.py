import os
from functools import reduce

with open(os.path.join(os.path.dirname(__file__), "input"), "r") as inputFile:
    inputString = [line.replace("\n", "") for line in inputFile.readlines()]


def h2b(hexa):
    return "".join((bin(int(char, 16))[2:].zfill(4) for char in hexa))


class Code:
    def __init__(self, string="") -> None:
        self.string = string

    def __repr__(self) -> str:
        return "(%s)%s" % (len(self.string), self.string)

    def __str__(self) -> str:
        return self.string

    def __int__(self) -> int:
        return int(self.string, 2) if bool(self) else 0

    def __bool__(self) -> bool:
        return bool(self.string)

    def __getitem__(self, key):
        return Code(self.string.__getitem__(key))

    def __getslice__(self, i, j):
        return self.__getitem__(slice(i, j))

    def __eq__(self, other: object) -> bool:
        if isinstance(other, str):
            return self.string == other
        elif isinstance(other, Code):
            return self.string == other.string
        else:
            raise ValueError()

    def __add__(self, other):
        if isinstance(other, str):
            return Code(self.string + other)
        elif isinstance(other, Code):
            return Code(self.string + other.string)
        else:
            raise ValueError()

    def __len__(self) -> int:
        return len(self.string)

    def take(self, end) -> str:
        segment = self.string[:end]
        self.string = self.string[end:]
        return Code(segment)

    def copy(self):
        return Code("".join(c for c in self.string))


class Packet:
    def __init__(self, bits) -> None:
        self.bits = Code(bits)
        self.bitsUsed = Code()
        self.encoded = Code(bits)
        self.litteralValue = Code()
        self.subPackets = []
        self._value = 0

    def __repr__(self) -> str:
        return "%s (%s)" % (self._value, self.bitsUsed)

    def parse(self):
        self.packetVersion = int(self.encoded.take(3))
        self.typeID = int(self.encoded.take(3))

        if self.typeID == TYPE_ID_LITTERAL_VALUE:
            self.parseLitteralValue()
        else:
            self.parseOperatorPacket()

        self.bitsUsed = self.bits[: (len(self.bits) - len(self.encoded))]

    def parseLitteralValue(self):
        segment = self.encoded.take(5)
        self.litteralValue += segment[1:]
        if segment[0] == LITTERAL_VALUE_PREFIX_CONTINUE:
            self.parseLitteralValue()

    def parseOperatorPacket(self):
        self.lengthTypeID = int(self.encoded.take(1))
        if self.lengthTypeID == LENGTH_TYPE_ID_15:  # header = 3+3+1+15 = 22
            self.parseSubPacketsByLength()
        if self.lengthTypeID == LENGTH_TYPE_ID_11:  # header = 3+3+1+11 = 18
            self.parseSubPacketsByAmount()

    def parseSubPacketsByLength(self):
        codeLength = int(self.encoded.take(15))
        code = self.encoded.take(codeLength)
        while code:
            code = self.parseSubPacketInCode(code.copy()).encoded

    def parseSubPacketsByAmount(self):
        codeAmount = int(self.encoded.take(11))
        for _ in range(codeAmount):
            subPacket = self.parseSubPacketInCode(self.encoded.copy())
            self.encoded.take(len(subPacket.bitsUsed))

    def parseSubPacketInCode(self, code):
        subPacket = Packet(str(code))
        subPacket.parse()
        self.subPackets.append(subPacket)
        return subPacket

    def getVersion(self):
        return sum((packet.getVersion() for packet in self.subPackets)) + self.packetVersion

    @staticmethod
    def getValue(packet):
        if not packet._value:
            if packet.litteralValue:
                packet._value = int(packet.litteralValue)
            else:
                operation = {
                    TYPE_ID_SUM: sum,
                    TYPE_ID_PRODUCT: lambda iterable: reduce(lambda a, b: a * b, iterable),
                    TYPE_ID_MINIMUM: min,
                    TYPE_ID_MAXIMUM: max,
                    TYPE_ID_GREATER_THAN: lambda iterable: int(next(iterable) > next(iterable)),
                    TYPE_ID_LESS_THAN: lambda iterable: int(next(iterable) < next(iterable)),
                    TYPE_ID_EQUAL_TO: lambda iterable: int(next(iterable) == next(iterable)),
                }[packet.typeID]
                packet._value = operation(map(Packet.getValue, packet.subPackets))
        return packet._value


TYPE_ID_LITTERAL_VALUE = 4
TYPE_ID_SUM = 0
TYPE_ID_PRODUCT = 1
TYPE_ID_MINIMUM = 2
TYPE_ID_MAXIMUM = 3
TYPE_ID_GREATER_THAN = 5
TYPE_ID_LESS_THAN = 6
TYPE_ID_EQUAL_TO = 7

LITTERAL_VALUE_PREFIX_CONTINUE = Code("1")

LENGTH_TYPE_ID_15 = 0
LENGTH_TYPE_ID_11 = 1


def examples(lines):
    for line in lines[7:-1]:
        packet = Packet(h2b(line))
        packet.parse()
        print("version: %s" % packet.getVersion())
        print("value: %s" % Packet.getValue(packet))


def answer1(line):
    packet = Packet(h2b(line))
    packet.parse()
    return packet.getVersion()


def answer2(line):
    packet = Packet(h2b(line))
    packet.parse()
    return Packet.getValue(packet)


examples(inputString)
print(answer1(inputString[-1]))
print(answer2(inputString[-1]))
