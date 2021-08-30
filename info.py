from solucao import *

import os
import sys
import timeit

import numpy as np

N = 1
R = 10


class HiddenPrints():
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout


print("## BFS")
with HiddenPrints():
    tempos = timeit.repeat("bfs('2_3541687')", "from solucao import bfs", number=N, repeat=R)

print("Tempo de execução: %.5fs +- %.5fs" % (np.average(tempos).item(), np.std(tempos).item()))
print("Custo:", len(bfs('2_3541687')))
print()

print("## DFS")
with HiddenPrints():
    tempos = timeit.repeat("dfs('2_3541687')", "from solucao import dfs", number=N, repeat=R)

print("Tempo de execução: %.5fs +- %.5fs" % (np.average(tempos).item(), np.std(tempos).item()))
print("Custo:", len(dfs('2_3541687')))
print()

print("## A* usando distância hamming")
with HiddenPrints():
    tempos = timeit.repeat("astar_hamming('2_3541687')", "from solucao import astar_hamming", number=N, repeat=R)

print("Tempo de execução: %.5fs +- %.5fs" % (np.average(tempos).item(), np.std(tempos).item()))
print("Custo:", len(astar_hamming('2_3541687')))
print()

print("## A* usando distância manhattan")
with HiddenPrints():
    tempos = timeit.repeat("astar_manhattan('2_3541687')", "from solucao import astar_manhattan", number=N, repeat=R)

print("Tempo de execução: %.5fs +- %.5fs" % (np.average(tempos).item(), np.std(tempos).item()))
print("Custo:", len(astar_manhattan('2_3541687')))
print()
