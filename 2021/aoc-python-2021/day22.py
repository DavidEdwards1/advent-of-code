import dataclasses
import itertools

from dataclasses import dataclass
from typing import List, Tuple, Union


@dataclass(frozen=True)
class Point:
    x: int
    y: int
    z: int

@dataclass(frozen=True)
class Cuboid:
    min: Point
    max: Point #this is an open interval, so this point is not included

    active: bool = True

def points_in_cuboid(cuboid: Cuboid):
    return (
        (cuboid.max.x - cuboid.min.x)
        * (cuboid.max.y - cuboid.min.y)
        * (cuboid.max.z - cuboid.min.z)
    )


def sorted_cuboids(cuboids: List[Cuboid]) -> List[Cuboid]:
    return sorted(cuboids, key=lambda cub: (cub.min.x, cub.min.y, cub.min.z))

def intersection(cuboids):
    cuboids = list(set(cuboids))

    if len(cuboids) == 1:
        return cuboids
    elif len(cuboids) == 2:
        cuboid1, cuboid2 = sorted_cuboids(cuboids)

        x_range = [
            max(cuboid1.min.x, cuboid2.min.x),
            min(cuboid1.max.x, cuboid2.max.x)
        ]

        y_range = [
            max(cuboid1.min.y, cuboid2.min.y),
            min(cuboid1.max.y, cuboid2.max.y)
        ]

        z_range = [
            max(cuboid1.min.z, cuboid2.min.z),
            min(cuboid1.max.z, cuboid2.max.z)
        ]

        x_range = [x_range[0], max(x_range)]
        y_range = [y_range[0], max(y_range)]
        z_range = [z_range[0], max(z_range)]

        if any([x_range[0] == x_range[1], y_range[0] == y_range[1], z_range[0] == z_range[1]]):
            # no cuboid
            return []
        else:
            return [
                Cuboid(
                    Point(x_range[0], y_range[0], z_range[0]),
                    Point(x_range[1], y_range[1], z_range[1])                )
            ]

    else:
        return intersection(intersection(cuboids[:2]) + cuboids[2:])

def inclusion_exclusion(cuboids, current_sets=[]):
    number_of_cuboids = len(cuboids)

    if number_of_cuboids == 0:
        cardinality = 0
    elif number_of_cuboids == 1:
        cardinality = sum(points_in_cuboid(cub) for cub in cuboids if cub.active)
    else:
        if cuboids[0].active:
            intersections = [inter for cub in cuboids[1:] for inter in intersection([cuboids[0],cub])]
        else:
            intersections = []
        cardinality = (
            inclusion_exclusion([cuboids[0]])
            - inclusion_exclusion(intersections)
            + inclusion_exclusion(cuboids[1:])
        )

    # print("Returning from inc/ex")
    # print(cuboids)
    # print(cardinality)
    return cardinality


def parse_input_line(line):
    instruction, cuboid_description = line.strip().split(" ")
    cuboid_description = [dim[2:].split("..") for dim in cuboid_description.split(",")]
    cuboid_description = [sorted([int(x) for x in bound]) for bound in cuboid_description]
    cuboid_description = [[x[i] + i for x in cuboid_description] for i in range(len(cuboid_description[0]))]
    cuboid_active = True if instruction == "on" else False
    cuboid = Cuboid(
        Point(*cuboid_description[0]),
        Point(*cuboid_description[1]),
        cuboid_active
    )
    return instruction, cuboid

def read_data(filename):
    with open(filename) as f:
        data = f.readlines()

    return [parse_input_line(line) for line in data]


if __name__ == "__main__":

    reboot_steps = read_data("data-day22.txt")

    for i in range(len(reboot_steps)+1):
        print(f"Considering {i} steps")
        cuboids = [step[1] for step in reboot_steps[:i]]
        print(inclusion_exclusion(cuboids))
