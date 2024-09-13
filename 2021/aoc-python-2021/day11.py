import numpy as np


def flash_at(x,y, octopii):
    for i in range(-1,2):
        for j in range(-1,2):
            flash_point_x = x+i
            flash_point_y = y+j
            if (
                (0 <= flash_point_x < octopii.shape[0])
                and ((0 <= flash_point_y < octopii.shape[1]))
            ):
                octopii[flash_point_x, flash_point_y] = octopii[flash_point_x, flash_point_y] + 1
    return octopii

def step(octopii):
    not_flashed = np.ones(octopii.shape)
    n_flashes = 0

    octopii = octopii + 1

    while ((octopii * not_flashed) > 9).any():
        points_to_flash = [(x,y) for x,y in zip(*np.where((octopii * not_flashed) > 9))]

        for x,y in points_to_flash:
            not_flashed[x, y] = 0
            n_flashes += 1
            octopii = flash_at(x,y, octopii)

    return (octopii * not_flashed), n_flashes



with open("data-day11-example.txt") as f:
    octopii = np.array([list(row.strip()) for row in f.readlines()], dtype=int)

n_steps = 100
total_flashes = 0

for i in range(n_steps):
    octopii, n_flashes = step(octopii)
    total_flashes = total_flashes + n_flashes

    print(f"Step {i+1}, flashes {n_flashes}, total_flashes {total_flashes}")


# Part 2
with open("data-day11.txt") as f:
    octopii = np.array([list(row.strip()) for row in f.readlines()], dtype=int)

i = 0
n_flashes = 0

while n_flashes != octopii.shape[0] * octopii.shape[1]:
    octopii, n_flashes = step(octopii)

    print(f"Step {i+1}, flashes {n_flashes}")
    i += 1
