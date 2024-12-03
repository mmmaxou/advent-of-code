import os

inputPath = os.path.join(os.path.dirname(__file__), "input")

with open(inputPath, "r") as inputFile:
    raw = inputFile.read()


def answer(iterable, topAmount):
    elfCalories = [
        sum([int(food) for food in elf.split("\n")]) for elf in iterable.split("\n\n")
    ]
    maxCalories = sum(sorted(elfCalories, reverse=True)[:topAmount])
    return maxCalories


print(answer(raw, 1))
print(answer(raw, 3))
