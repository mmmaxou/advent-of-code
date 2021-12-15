import heapq
import os


with open(os.path.join(os.path.dirname(__file__), "input"), "r") as inputFile:
    inputString = inputFile.read()


def parseInput(raw_data):
    res = []
    for line in raw_data.split('\n'):
        res.append(list(map(int, line)))
    return res


CAVERN = parseInput(inputString)
N, M = len(CAVERN), len(CAVERN[0])


def dijkstra(graph):
    rows, cols = len(graph), len(graph[0])
    costs = {}
    heap = [(0, 0, 0)]
    while heap:
        cost, i, j = heapq.heappop(heap)
        if (i, j) == (rows - 1, cols - 1):
            return cost
        for ni, nj in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
            if 0 <= ni < rows and 0 <= nj < cols:
                ncost = cost + graph[ni][nj]
                if costs.get((ni, nj), float('inf')) <= ncost:
                    continue
                costs[(ni, nj)] = ncost
                heapq.heappush(heap, (ncost, ni, nj))


def answer1():
    return dijkstra(CAVERN)


def answer2():
    rows, cols = len(CAVERN) * 5, len(CAVERN[0]) * 5
    expanded = [[0 for _ in range(cols)] for _ in range(rows)]
    for i in range(rows):
        for j in range(cols):
            distance = i // N + j // M
            weight = CAVERN[i % N][j % M] + distance
            weight = weight % 9 or weight
            expanded[i][j] = weight
    return dijkstra(expanded)


print(f'Part 1: {answer1()}')
print(f'Part 2: {answer2()}')