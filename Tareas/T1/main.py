from Enigma import Enigma, abc
from solver import Solver
import sys
from functools import reduce


def process_quijote(filepath):
    confs, texts, cifrs = [], [], []
    with open(filepath, "r") as file:
        for line in file.readlines():
            [conf, text, cifr] = line.split(";")
            confs.append(int(conf[1]))  # guarda el número de discos
            texts.append(text)
            cifrs.append(cifr[:-1])  # sacamos el \n
    return confs, texts, cifrs


keys = [[0, 12, 6, 9, 16, 25, 14, 2, 27, 10, 3, 21, 20, 19, 8, 4, 5, 1, 7, 26, 24, 23, 11, 13, 22, 15, 18, 17],
        [23, 22, 3, 25, 16, 6, 24, 4, 11, 8, 20, 10, 7, 26,
            14, 2, 15, 12, 17, 21, 19, 13, 0, 9, 5, 18, 1, 27],
        [0, 17, 7, 8, 1, 26, 13, 6, 5, 24, 15, 18, 27, 2, 16,
            25, 3, 9, 12, 22, 11, 23, 21, 4, 20, 19, 14, 10],
        [18, 26, 20, 14, 2, 23, 16, 17, 25, 3, 15, 21, 1, 7,
            10, 19, 22, 8, 5, 13, 24, 11, 4, 6, 9, 0, 12, 27],
        [17, 6, 19, 11, 23, 2, 21, 13, 27, 9, 18, 24, 0, 4, 8,
            26, 12, 5, 14, 1, 16, 7, 3, 22, 15, 10, 25, 20],
        [4, 22, 26, 16, 19, 0, 9, 2, 14, 3, 24, 13, 1, 15, 18,
            12, 21, 17, 23, 7, 11, 6, 20, 27, 8, 10, 5, 25]
        ]

confs, texts, cifrs = process_quijote(sys.argv[1])

number_of_discs = sys.argv[2]

enigma = Enigma(keys[:number_of_discs])

solver = Solver(enigma, confs, texts, cifrs)

print(solver.solve())
