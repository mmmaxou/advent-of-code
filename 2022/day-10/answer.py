import os
from dataclasses import dataclass, field
from typing import List

with open(os.path.join(os.path.dirname(__file__), "input"), "r") as inputFile:
    inputLines = [line.strip() for line in inputFile.readlines() if line]


@dataclass
class Signal:
    cycle: int
    register: int
    strength = 0

    def __post_init__(self):
        self.strength = self.cycle * self.register


@dataclass
class CRT:
    pixels: List[str] = field(default_factory=lambda: [""])

    def drawPixel(self, register: int) -> None:
        self.pixels[-1] += "#" if abs(len(self.pixels[-1]) - register) <= 1 else "."
        if len(self.pixels[-1]) == 40:
            self.pixels.append("")

    def __str__(self) -> str:
        return "\n".join(self.pixels)


class CPU:
    def __init__(self) -> None:
        self.states: List[Signal] = [Signal(cycle=0, register=1)]
        self.instructions: List[str] = []
        self.interestingSignals: List[Signal] = []
        self.crt = CRT()

    def parseLine(self, line) -> None:
        """Transform line into instructions"""
        if line == "noop":
            return self.instructions.append("noop")
        self.instructions.append("start " + line)
        self.instructions.append("end " + line)

    def executeInstructions(self) -> None:
        for cycle, line in enumerate(self.instructions, start=1):
            register = self.states[-1].register

            self.crt.drawPixel(register)

            # Read is **during** the cycle, not after the cycle
            if cycle % 40 == 20:
                self.interestingSignals.append(Signal(register=register, cycle=cycle))

            if line.startswith("end "):
                register += int(line.split(" ")[-1])
            self.states.append(Signal(register=register, cycle=cycle))

    def sumInterestingSignals(self) -> int:
        return sum([signal.strength for signal in self.interestingSignals])


def answer(iterable):
    cpu = CPU()
    [cpu.parseLine(line) for line in iterable]
    cpu.executeInstructions()

    # Answer 1
    print(cpu.sumInterestingSignals())

    # Answer 2
    print(cpu.crt)


answer(inputLines)
