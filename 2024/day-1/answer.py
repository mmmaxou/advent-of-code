import os
import functools
import numpy as np


inputPath = os.path.join(os.path.dirname(__file__), "input")

with open(inputPath, "r") as inputFile:
    raw = inputFile.read()


def answer(iterable):
    return np.abs(
        np.diff(
            np.sort(np.fromstring(iterable, sep=" ", dtype=int).reshape(-1, 2), axis=0),
            axis=1,
        )
    ).sum()


print(answer(raw))


def answer_bis(iterable):
    data = np.fromstring(iterable, sep=" ", dtype=int).reshape(-1, 2)
    array = np.rot90(
        np.array(
            np.unique(
                data[:, 1],
                return_counts=True,
            )
        )
    )
    d = dict(array)

    res = np.vectorize(lambda x: x * d.get(x, 0))(data[:, 0]).sum()

    return res


print(answer_bis(raw))
