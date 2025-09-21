import itertools
from chunk_0 import chunk0_solutions, literals_in_chunk0
from chunk_1 import chunk1_solutions, literals_in_chunk1
from chunk_2 import chunk2_solutions, literals_in_chunk2
from chunk_3 import chunk3_solutions, literals_in_chunk3

#print("Chunk 0 solutions: ")
#print(chunk0_solutions)

#print("\n\nChunk 1 solutions: ")
#print(chunk1_solutions)

#print("\n\nChunk 2 solutions: ")
#print(chunk2_solutions)

#print("\n\nChunk 3 solutions: ")
#print(chunk3_solutions)

def one_set_literal_fix(literals, solutions):
    fixed_lits = []
    for lit in literals:
        if lit in solutions[0]:
            first_sign = 1
        elif -lit in solutions[0]:
            first_sign = -1
        else:
            raise ExceptionType("Literal not in solutions -- this shouldn't happen ")
        fixed = True
        for sol in solutions[1:]:
            if (first_sign * lit) not in sol:
                fixed = False
                break # exit the loop 
        if fixed == True:
            fixed_lits.append(first_sign * lit)
    return fixed_lits



literals_dict = {0: literals_in_chunk0,
                 1: literals_in_chunk1,
                 2: literals_in_chunk2,
                 3: literals_in_chunk3
                 }

solution_dict = {
    0: chunk0_solutions,
    1: chunk1_solutions,
    2: chunk2_solutions,
    3: chunk3_solutions
}

intersection_list = []

for (i, set1), (j, set2) in itertools.combinations(literals_dict.items(), 2):
    intersection_size = len(set1 & set2)
    intersection_list.append(((i, j), set1, set2, (set1 & set2), intersection_size))

# sort by intersection size, largest first
intersection_list.sort(key=lambda x: x[4], reverse=True)

# print results
'''
for (i, j), set1, set2, size in intersection_list:
    print(f"Pair: chunk {i} and chunk {j}")
    print("Intersection size:", size)
    print("Set1:", set1)
    print("Set2:", set2)
    print("---")
'''

print("Fixing the literals across the single solution sets, we learn:")
print(f"Chunk 0 fixes {one_set_literal_fix(literals_in_chunk0, chunk0_solutions)}")
print(f"Chunk 1 fixes {one_set_literal_fix(literals_in_chunk1, chunk1_solutions)}")
print(f"Chunk 2 fixes {one_set_literal_fix(literals_in_chunk2, chunk2_solutions)}")
print(f"Chunk 3 fixes {one_set_literal_fix(literals_in_chunk3, chunk3_solutions)}\n\n")

## approach 1: iterate through all of the tuples and see which literals I can fix that way
all_fixed_lits = []

for sets in intersection_list:
    fixed_lits = []
    indices = sets[0]
    intersection = sets[3]
    print(f"Intersection of chunk {indices[0]} and chunk {indices[1]} = {intersection}")
    print(f"Intersection size: {sets[4]}") 
    sols = solution_dict[indices[0]] + solution_dict[indices[1]] # combine all solutions into one list 
   
    for lit in intersection:
        if lit in sols[0]:
            first_sign = 1
        elif -lit in sols[0]:
            first_sign = -1
        else:
            raise ExceptionType("Literal not in solutions -- this shouldn't happen ")
        fixed = True
        print(f"Checking for {first_sign * lit} across solutions")
        for sol in sols[1:]:
            if (first_sign * lit) not in sol:
                fixed = False
                print(f"{sol} exists and breaks the pattern \n")
                break # exit the loop 

        if fixed == True:
            fixed_lits.append(first_sign * lit)

    all_fixed_lits.append(fixed_lits)
    print("\n\n")

print(f"Through the intersection method, we fix the following boolean literals: {all_fixed_lits}")
