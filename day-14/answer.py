import os
from os import write
from parse import compile

inputPath = os.path.join(os.path.dirname(__file__), "input")

with open(inputPath, "r") as inputFile:
    groups = inputFile.read().split("\nmask")
    groups[0] = groups[0].replace("mask", "")

maskParse = compile(" = {mask:w}")
memParse = compile("mem[{adress:d}] = {value:d}")


class Solver:
    def parseGroups(self, groups):
        groupsDatas = []
        for group in groups:
            lines = group.split("\n")
            groupData = {"mask": [], "lines": []}
            for line in lines:
                if line.startswith(" ="):
                    mask = list(maskParse.parse(line)["mask"])
                    groupData["mask"] = mask
                elif line.startswith("mem"):
                    adress, value = memParse.parse(line).named.values()
                    groupData["lines"].append({"adress": adress, "value": value})
            groupsDatas.append(groupData)
        return groupsDatas

    def fillMemory(self, groups):
        memory = {}
        for group in groups:
            mask = group["mask"]
            for line in group["lines"]:
                value = self.applyMaskToValue(mask, line["value"])
                self.changeMemory(memory, mask, line["adress"], value)
        return memory

    def applyMaskToValue(self, mask, value):
        binary = list("{0:b}".format(value).rjust(36, "0"))
        masked = [bit if bitmask == "X" else bitmask for bitmask, bit in zip(mask, binary)]
        number = int("".join(masked), 2)
        return number

    def changeMemory(self, memory, mask, adress, value):
        memory[adress] = value


class Solver2(Solver):
    def applyMaskToAdress(self, mask, adress):
        binary = list("{0:b}".format(adress).rjust(36, "0"))
        masked = [bit if bitmask == "0" else bitmask for bitmask, bit in zip(mask, binary)]
        return masked

    def applyMaskToValue(self, mask, value):
        return value

    def changeMemory(self, memory, mask, adress, value, shallApply=True, maskedAdressStart=0):
        if shallApply:
            maskedAdress = self.applyMaskToAdress(mask, adress)
        else:
            maskedAdress = adress
        changed = 0
        for index, bit in enumerate(maskedAdress[maskedAdressStart:]):
            if bit == "X":
                nIndex = maskedAdressStart + index
                adress0 = maskedAdress[:nIndex] + ["0"] + maskedAdress[nIndex + 1 :]
                adress1 = maskedAdress[:nIndex] + ["1"] + maskedAdress[nIndex + 1 :]
                changed += self.changeMemory(memory, maskedAdress, adress0, value, False, nIndex + 1)
                changed += self.changeMemory(memory, maskedAdress, adress1, value, False, nIndex + 1)
                break
        if changed == 0:
            writeAdress = int("".join(maskedAdress), 2)
            memory[writeAdress] = value
            return 1
        else:
            return changed


def solve1():
    solver = Solver()
    groupsDatas = solver.parseGroups(groups)
    memory = solver.fillMemory(groupsDatas)
    result = sum(memory.values())
    return result


def solve2():
    solver = Solver2()
    groupsDatas = solver.parseGroups(groups)
    memory = solver.fillMemory(groupsDatas)
    result = sum(memory.values())
    return result


print(solve1())
print(solve2())
