import numpy as np

def damp_x(x):
    if x > 0:
        x = x - 1
    elif x < 0:
        x = x + 1
    return x

def step(position, velocity):
    position = position + velocity
    velocity = np.array([damp_x(velocity[0]), velocity[1]-1])
    return position, velocity

def target_missed(target, position, velocity):
    if position[0] > target[0][1]:
        missed = True
    elif position[1] < target[1][0]:
        missed = True
    else:
        missed = False

    return missed

def in_target(target, position):
    return (
        (target[0][0] <= position[0] <= target[0][1])
        and (target[1][0] <= position[1] <= target[1][1])
    )

def calculate_trajectory(initial_position, initial_velocity):
    position = initial_position
    velocity = initial_velocity
    success = in_target(target, position)
    trajectory = []

    while not (target_missed(target, position, velocity) or success) :
        position, velocity = step(position, velocity)
        success = in_target(target, position)
        trajectory.append(position)

    return trajectory, success


initial_position = np.array([0, 0])

with open("data-day17.txt") as f:
    raw_string = f.readline().strip()


target = [
    tuple(int(t) for t in tp.strip()[2:].split(".."))
    for tp in raw_string[12:].split(", ")
]

successful_trajectories = []
max_heights = []
successful_ivs = []

# for the y range, if the y velocity is positive then when it comes back through
# zero (which it will) the y velocity will be -1 * start which means if that if
# it is larger in absolute terms than the minimum of the target it'll skip over
# it. Can also assume that the y velocity should be positive otherwise 0 is max
# height
for vy in range(target[1][0], abs(target[1][0])+1):
    for vx in range(0, target[0][1]+1):
        initial_velocity = np.array([vx, vy])

        trajectory, ok = calculate_trajectory(initial_position, initial_velocity)
        if ok:
            successful_trajectories.append(trajectory)
            max_height = max(p[1] for p in trajectory)
            max_heights.append(max_height)
            successful_ivs.append(initial_velocity)

print("Max height reached: ", max(max_heights))
print("Count of different initial velocities: ", len(successful_ivs))
