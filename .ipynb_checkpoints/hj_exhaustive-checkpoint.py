from itertools import product
from sympy import symbols
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from pysat.solvers import Solver
import time
import tracemalloc


### functions
def combinatorial_line(word, alphabet):
    lines = []
    for a in alphabet:
        new_word = list(a if val == x else val for val in word)  # tuple instead of list
        lines.append(new_word)
    return lines

def create_var_map(tuples):
    """
    Input: list of tuples (each tuple can have arbitrary length)
    Output: dictionary mapping each tuple -> unique integer literal
    """
    return {t: i+1 for i, t in enumerate(tuples)}


### code 
x = symbols('x')
m = 2 # m is the potential Hales-Jewett number 
n = 3 # n is the length of the alphabet
c = 2 # don't actually use this, just a reminder that we set c = 2
# so, we're looking at HJ(n,2)
hales_found = False
alphabet = list(range(1, n+1))

print(f"Solving for HJ({n}, 2)\n", flush = True)

while not hales_found:
    print(f"Case: m = {m}", flush = True)
    tracemalloc.start() # track memory for each iteration
    start_time = time.time() # track time for each iteration
    configs = []
    variable_words = []
    cells = list(product(alphabet, repeat=m))
    print(f"There are {len(cells)} cells in this hypercube.", flush = True)
    #for c in cells:
    #    print(c)

    for mask in product([0, 1], repeat=m):
        if sum(mask) == 0:  # skip all-blank
            continue
        config = [x if bit else 0 for bit in mask]
        configs.append(config)

    print(f"There are {len(configs)} variable word structures.", flush=True)
    #for c in configs:
    #    print(c)

    for c in configs:
        zero_positions = [i for i, val in enumerate(c) if val == 0]
        k = len(zero_positions)
        
        for fill in product(alphabet, repeat=k):
            word = list(c)  
            for pos, val in zip(zero_positions, fill):
                word[pos] = val
            variable_words.append(word)  

    print(f"For m = {m} and n = {n}, there are {len(variable_words)} variable words.", flush=True)



    combinatorial_lines = []
    for vw in variable_words:
        combinatorial_lines.append(combinatorial_line(vw, alphabet))
    
    print(f"We generated {len(combinatorial_lines)} combinatorial lines.", flush = True)
    if m == 5:
        for cl in combinatorial_lines:
            print(cl)

    map = create_var_map(cells)
    # print("Below is the tuple to integer mapping: \n",map)


    boolean_literals = list(map.values())
    # print("Below is a list of boolean literals:\n", boolean_literals)

    solver = Solver(name='glucose4') # just choosing a random solver for now
    print("GENERATING LITERALS & CLAUSES", flush=True)


    for cl in combinatorial_lines: # for each combinatorial line, we are going to generate 2 clauses
        literals = [map[tuple(c)] for c in cl] # convert all to literals via my integer mapping
        negated_literals = [-lit for lit in literals] 
        clause_1 = literals # returns false if the whole line is monochromatic blue 
        clause_2 = negated_literals # returns false if the whole line is monochromatic red
        solver.add_clause(clause_1)
        solver.add_clause(clause_2)
        print(clause_1)
        print(clause_2)

    print(f"There are {len(combinatorial_lines)*2} clauses in our CNF formula.", flush = True)
    print("Testing solver", flush=True)


    solver.add_clause([1]) # symmetry breaking?


    solution_count = 0

    for model in solver.enum_models():
            print(model) 
            solution_count += 1

    print("solution count:", solution_count)
    if solution_count > 0:
        
        m += 1
        print("found solutions -- incrementing")
        if m == 3:
            hales_found = True
    else:
        hales_found = True
        print("no solutions, hales jewett number m =", m, "found.")
    
    if m > 5:
        print("STOPPING FOR SAKE OF MY COMPUTER")
        break

    end_time = time.time()
    print("Solver runtime:", end_time - start_time, "seconds\n\n", flush=True)

'''


    if solver.solve():
        model = solver.get_model()    # returns a list of integers
        print("Satisfiable -- incrementing m", flush=True)
        m += 1
        print("solution:")
        print(model, "\n\n")
    else:
        print(f"Unsatisfiable, HJ(2,{n}) = {m}", flush=True)
        hales_found = True
    solver.delete()
    end_time = time.time()

    current, peak = tracemalloc.get_traced_memory()
    print(f"Current memory usage: {current / 1024:.2f} KB", flush=True)
    print(f"Peak memory usage: {peak / 1024:.2f} KB", flush=True)

    tracemalloc.stop()
    print("Solver runtime:", end_time - start_time, "seconds\n\n", flush=True)


    
fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")

# plot each line with a different color
for line in combinatorial_lines:
    xs, ys, zs = zip(*line)
    ax.plot(xs, ys, zs, marker="o")

ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")
plt.savefig("lines_len3_3d.png") 
plt.show()
'''
