import os

template = """import os

inputPath = os.path.join(os.path.dirname(__file__), "input")

with open(inputPath, "r") as inputFile:
    raw = inputFile.read()


def answer(iterable):
    return

print(answer(raw))
print(answer(raw))
"""

DIR = os.path.dirname(__file__)
year = "2024"

if not os.path.isdir(os.path.join(DIR, year)):
    os.makedirs(os.path.join(DIR, year))

days = [day for day in os.listdir(year) if day.startswith("day-")]
newDay = len(days) + 1
newDayStr = "day-%s" % newDay

if not os.path.isdir(os.path.join(DIR, year, newDayStr)):
    os.makedirs(os.path.join(DIR, year, newDayStr))

if not os.path.isfile(os.path.join(DIR, year, newDayStr, "answer.py")):
    with open(os.path.join(DIR, year, newDayStr, "answer.py"), "w") as fileIO:
        fileIO.write(template)

if not os.path.isfile(os.path.join(DIR, year, newDayStr, "input")):
    with open(os.path.join(DIR, year, newDayStr, "input"), "w") as fileIO:
        fileIO.write("")
