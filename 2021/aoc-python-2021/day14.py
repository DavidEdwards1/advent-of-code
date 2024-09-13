import collections
import re


def insertion_step(starting_polymer, insertion_instructions):

    insertions = collections.defaultdict(int)

    for target, insertion in insertion_instructions.items():
        if target in starting_polymer:
            insertions[target] += -1 * starting_polymer[target]
            insertions[insertion[0]] += starting_polymer[target]
            insertions[insertion[1]] += starting_polymer[target]

    new_polymer = {**starting_polymer, **insertions}
    for k in new_polymer.keys():
        if (k in starting_polymer) and (k in insertions):
            new_polymer[k] = starting_polymer[k] + insertions[k]

    return new_polymer

with open("data-day14.txt") as f:
    inputs = [l.strip() for l in f.readlines()]

starting_polymer = inputs[0]
insertion_instructions = [inst.split("->") for inst in inputs[2:]]
insertion_instructions = {(k.strip()[0],k.strip()[1]): ((k.strip()[0], v.strip()), (v.strip(), k.strip()[1])) for k,v in insertion_instructions}

final_polymer = collections.Counter(zip(starting_polymer, starting_polymer[1:]))

for i in range(10):
    final_polymer = insertion_step(final_polymer, insertion_instructions)
    print(f"After step {i}, length of polymer {sum(v for v in final_polymer.values())+1}")

# note that the last char will _always_ be the last char
last_char = starting_polymer[-1]

element_counts = collections.defaultdict(int)
for k,v in final_polymer.items():
    element_counts[k[0]] += v

element_counts[last_char] += 1
element_counts = sorted([(k,v) for k,v in element_counts.items()], key= lambda x: x[1], reverse=True)


print("\nAfter 10 steps")
print("======================")
print(f"Most common element: {element_counts[0][0]} with {element_counts[0][1]} occurances")
print(f"Least common element: {element_counts[-1][0]} with {element_counts[-1][1]} occurances")
print(f"Difference between counts: {element_counts[0][1] - element_counts[-1][1]}")

for i in range(10, 40):
    final_polymer = insertion_step(final_polymer, insertion_instructions)
    print(f"After step {i}, length of polymer {sum(v for v in final_polymer.values())+1}")

element_counts = collections.defaultdict(int)
for k,v in final_polymer.items():
    element_counts[k[0]] += v

element_counts[last_char] += 1
element_counts = sorted([(k,v) for k,v in element_counts.items()], key= lambda x: x[1], reverse=True)

print("\nAfter 40 steps")
print("======================")
print(f"Most common element: {element_counts[0][0]} with {element_counts[0][1]} occurances")
print(f"Least common element: {element_counts[-1][0]} with {element_counts[-1][1]} occurances")
print(f"Difference between counts: {element_counts[0][1] - element_counts[-1][1]}")
