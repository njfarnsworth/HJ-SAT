from set_up import chunk_1, map, tuple_to_litmap
from pysat.solvers import Solver

solver = Solver(name='glucose4')

literals_in_chunk1 = set()
x1_in_lits = False  # use this to determine whether we'll symmetry block x_1

for cl in chunk_1: # collect all of the literals 
    literals = [map[tuple(c)] for c in cl] # convert all to literals via my integer mapping
    literals_in_chunk1.update(literals)

lit_map = {orig: i+1 for i, orig in enumerate(literals_in_chunk1)} # generate the lit map
rev_map = {v: k for k, v in lit_map.items()} # generate the reverse map

if 1 in literals_in_chunk1:
    print("Chunk 1: Performing symmetry blocking on x_1")
    x1_in_lits = True
    
print("Chunk 1 literals before map: ", literals_in_chunk1)
print("Chunk 1 literals after map: ", lit_map)

for cl in chunk_1: 
    literals =  tuple_to_litmap(cl, map, lit_map) # going from tuple to lit map 
    negated_literals = [-lit for lit in literals] 
    clause_1 = literals # returns false if the whole line is monochromatic blue 
    clause_2 = negated_literals # returns false if the whole line is monochromatic red
    solver.add_clause(clause_1)
    solver.add_clause(clause_2)

if x1_in_lits:
    solver.add_clause([1])

solution_count = 0
chunk1_solutions = []

for model in solver.enum_models():
    mapped_model = set(
        rev_map[abs(lit)] if lit > 0 else -rev_map[abs(lit)]
        for lit in model if abs(lit) in rev_map
    )
    chunk1_solutions.append(mapped_model)
    solution_count += 1

print(f"Found {solution_count} solutions in chunk 1\n\n")
