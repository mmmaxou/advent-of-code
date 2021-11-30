import os
import re
import sys
import traceback

REQUIRED_FIELDS = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]
VALID_COLORS = "amb blu brn gry grn hzl oth".split(" ")

inputPath = os.path.join(os.path.dirname(__file__), "input")

with open(inputPath, "r") as inputFile:
    lines = [line.strip() for line in inputFile.readlines() if line]


def parseLines(lines):
    passports = []
    batch = []
    for line in lines:
        if line == "":
            fields = {}
            for field in batch:
                identifier, value = field.split(":")
                fields[identifier] = value
            passports.append(fields)
            batch = []
        else:
            for field in line.split(" "):
                batch.append(field)
    return passports


def isValid(passport):
    keys = passport.keys()
    for field in REQUIRED_FIELDS:
        if field not in keys:
            return False
    return True


def isValid2(passport):
    assert isValid(passport)

    # byr (Birth Year) - four digits; at least 1920 and at most 2002.
    byr = passport["byr"]
    assert re.match(r"^[0-9]{4,4}$", byr)
    assert int(byr) >= 1920
    assert int(byr) <= 2002

    # iyr (Issue Year) - four digits; at least 2010 and at most 2020.
    iyr = passport["iyr"]
    assert re.match(r"^[0-9]{4,4}$", iyr)
    assert int(iyr) >= 2010
    assert int(iyr) <= 2020

    # eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
    eyr = passport["eyr"]
    assert re.match(r"^[0-9]{4,4}$", eyr)
    assert int(eyr) >= 2020
    assert int(eyr) <= 2030

    # hgt (Height) - a number followed by either cm or in:
    #     If cm, the number must be at least 150 and at most 193.
    #     If in, the number must be at least 59 and at most 76.
    hgt = passport["hgt"]
    assert re.match(r"^\d+(cm|in)$", hgt)
    if hgt[-2:] == "cm":
        hgtInt = int(hgt[:-2])
        assert hgtInt >= 150
        assert hgtInt <= 193
    elif hgt[-2:] == "in":
        hgtInt = int(hgt[:-2])
        assert hgtInt >= 59
        assert hgtInt <= 76

    # hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
    hcl = passport["hcl"]
    assert len(hcl) == 7
    assert hcl[0] == "#"
    assert re.match(r"^[0-9a-f]{6,6}$", hcl[1:])

    # ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
    ecl = passport["ecl"]
    assert ecl in VALID_COLORS

    # pid (Passport ID) - a nine-digit number, including leading zeroes.
    pid = passport["pid"]
    assert len(pid) == 9
    assert re.match(r"^\d+$", pid)


def isReallyValid(passport):
    try:
        isValid2(passport)
    except AssertionError:
        _, _, tb = sys.exc_info()
        tb_info = traceback.extract_tb(tb)
        _, line, _, text = tb_info[-1]
        print("An error occurred on line {} in statement {}".format(line, text))
        return False
    return True


def solve():
    passports = parseLines(lines)
    valids = [isReallyValid(passport) for passport in passports]
    count = sum(valids)
    return count


print(solve())
