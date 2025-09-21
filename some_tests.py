from itertools import product
from sympy import symbols
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time
import tracemalloc

n = 4  # number of variables
combinations = []

for p in product([-1, 1], repeat=n-1):
    combo = [1] + list(p)
    # skip all-zeroes (after x1) and all-ones
    if all(x == 0 for x in combo[1:]) or all(x == 1 for x in combo[1:]):
        continue
    combinations.append(combo)

for c in combinations:
    print(c)