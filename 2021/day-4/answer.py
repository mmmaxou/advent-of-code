import os

inputPath = os.path.join(os.path.dirname(__file__), "input")


class Board(object):
    def __init__(self):
        super().__init__()
        self.lines = []
        self.transposeLines = []
        self.numbers = set()
        self.winnerNumber = 0

    def initLine(self, line):
        self.lines.append([int(n) for n in line.split()])

    def addNumber(self, number):
        self.numbers.add(number)

    def createTranspose(self):
        rows = []
        for line in self.lines:
            for index, value in enumerate(line):
                if len(rows) == index:
                    rows.append([])
                rows[index].append(value)
        self.transposeLines = rows

    def isWinner(self):
        for x in range(5):
            xWin = 0
            yWin = 0
            for y in range(5):
                if self.lines[x][y] in self.numbers:
                    xWin += 1
                if self.transposeLines[x][y] in self.numbers:
                    yWin += 1

            if xWin == 5 or yWin == 5:
                return True
        return False

    def addWinnerNumber(self, number):
        self.winnerNumber = number

    def computeScore(self):
        notValidated = []
        for x in range(5):
            for y in range(5):
                if self.lines[x][y] not in self.numbers:
                    notValidated.append(self.lines[x][y])
        return sum(notValidated) * self.winnerNumber


with open(inputPath, "r") as inputFile:
    lines = [line.replace("\n", "") for line in inputFile.readlines()]
    randomNumbers = [int(n) for n in lines[0].split(",")]

    # Create boards
    boards = []
    currentBoard = None
    for line in lines[1:]:
        if line == "":
            if currentBoard:
                currentBoard.createTranspose()
                boards.append(currentBoard)
            currentBoard = Board()
        else:
            currentBoard.initLine(line)


def answer1(numbers):
    winners = []
    for number in numbers:
        for board in boards:
            board.addNumber(number)
            if board.isWinner():
                board.addWinnerNumber(number)
                winners.append(board)
        if winners:
            break
    return winners[0].computeScore()


def answer2(numbers):
    winners = []
    for number in numbers:
        for board in boards:
            board.addNumber(number)
            if board.isWinner() and not board.winnerNumber:
                board.addWinnerNumber(number)
                winners.append(board)
        if len(winners) == len(boards):
            break
    return winners[-1].computeScore()


print(answer1(randomNumbers))
print(answer2(randomNumbers))
