import numpy as np

def evolve(colony):
    return (
        np.array((*colony[1:], 0))
        + colony[0] * np.array((0, 0, 0, 0, 0, 0, 1, 0, 1))
    )

def run_for(n, colony):
    for i in range(n):
        colony = evolve(colony)

    return colony

with open("data-day06.txt") as f:
    lantern_fish_ages = np.array([int(x) for x in f.readline().strip().split(",")])

colony = np.zeros(9, dtype=int)

for lfa in lantern_fish_ages:
    colony[lfa] = colony[lfa] + 1

print(run_for(80, colony).sum())
print(run_for(256, colony).sum())
