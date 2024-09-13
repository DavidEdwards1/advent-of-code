import numpy as np

def positions_from_file(filename):
    with open(filename) as f:
        positions = np.array([int(x) for x in f.readline().strip().split(",")])

    return positions

def sum_to_n(n):
    return n * (n+1) // 2

def simple_cost(ps: np.ndarray, align: int):
    return np.abs(ps - align).sum()

def complicated_cost(ps: np.ndarray, align: int):
    steps = np.abs(ps - align)
    return sum_to_n(steps).sum()

crab_positions = positions_from_file("data-day07.txt")

possible_aligns = np.arange(np.min(crab_positions), np.max(crab_positions))
simple_costs = np.zeros(possible_aligns.shape)
complicated_costs = np.zeros(possible_aligns.shape)

for i, al in enumerate(possible_aligns):
    simple_costs[i] = simple_cost(crab_positions, al)
    complicated_costs[i] = complicated_cost(crab_positions, al)

print("Part 1")
print("======")
print("Align for lowest cost: ", possible_aligns[np.argmin(simple_costs)])
print("Cost for that alignment:", np.min(simple_costs))

print("Part 2")
print("======")
print("Align for lowest cost: ", possible_aligns[np.argmin(complicated_costs)])
print("Cost for that alignment:", np.min(complicated_costs))
