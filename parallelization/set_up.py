from itertools import product
from sympy import symbols
import numpy as np

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

def tuple_to_litmap(cl, map, lit_map):
    """
    Map a tuple -> var_map ID -> lit_map value
    """
    literals = [map[tuple(c)] for c in cl]
    literals = [lit_map[l] for l in literals]
    return literals


def split_into_chunks(lst, num_chunks):
    n = len(lst)
    chunk_sizes = [(n + i) // num_chunks for i in range(num_chunks)]
    chunks = []
    start = 0
    for size in chunk_sizes:
        chunks.append(lst[start:start + size])
        start += size
    return chunks



x = symbols('x')
m = 2 # m is the potential Hales-Jewett number 
n = 3 # n is the length of the alphabet
c = 2 # don't actually use this, just a reminder that we set c = 2
# so, we're looking at HJ(n,2)
print(f"Generating combinatorial lines and boolean literals for {m} = HJ({n},2)")

alphabet = list(range(1, n+1))
configs = []
variable_words = []
cells = list(product(alphabet, repeat=m))

for mask in product([0, 1], repeat=m):
    if sum(mask) == 0:  # skip all-blank
        continue
    config = [x if bit else 0 for bit in mask]
    configs.append(config)

for c in configs:
    zero_positions = [i for i, val in enumerate(c) if val == 0]
    k = len(zero_positions)
        
    for fill in product(alphabet, repeat=k):
        word = list(c)  
        for pos, val in zip(zero_positions, fill):
            word[pos] = val
        variable_words.append(word)  

combinatorial_lines = [] # create the combinatorial lines
for vw in variable_words:
    combinatorial_lines.append(combinatorial_line(vw, alphabet))

map = create_var_map(cells) # define the map from line to boolean

for cl in combinatorial_lines: # for each combinatorial line, we are going to generate 2 clauses
    literals = [map[tuple(c)] for c in cl]

combinatorial_chunks = split_into_chunks(combinatorial_lines, 4) # create the chunks
chunk_0 = combinatorial_chunks[0]
print(f"Chunk 0 has {len(chunk_0)} lines:")
for lines in chunk_0:
    print(lines)
chunk_1 = combinatorial_chunks[1]
print(f"\n\nChunk 1 has {len(chunk_1)} lines")
for lines in chunk_1:
    print(lines)
chunk_2 = combinatorial_chunks[2]
print(f"\n\nChunk 2 has {len(chunk_2)} lines")
for lines in chunk_2:
    print(lines)
chunk_3 = combinatorial_chunks[3]
print(f"\n\nChunk 3 has {len(chunk_3)} lines")
for lines in chunk_3:
    print(lines)
print("\n\n")

