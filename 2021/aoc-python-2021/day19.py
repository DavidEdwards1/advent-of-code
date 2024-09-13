import itertools

from math import cos, pi, sin
from os import read
from typing import List, Tuple


def generate_rotation_matrix_3d(alpha, beta, gamma):
    """
    The inputs are the number of integer clockwise rotations in each direction
    Since we know we are only interested in integer numbers of pi/2 rotations we
    also know that the values are always integers
    """
    a,b,g = alpha * pi/2, beta * pi/2, gamma * pi/2
    return [
        [int(cos(a) * cos(b)), int(cos(a)*sin(b)*sin(g) - sin(a)*cos(g)), int(cos(a)*sin(b)*cos(g) + sin(a)*sin(g))],
        [int(sin(a) * cos(b)), int(sin(a)*sin(b)*sin(g) + cos(a)*cos(g)), int(sin(a)*sin(b)*cos(g) - cos(a)*sin(g))],
        [int(-sin(b)), int(cos(b) * sin(g)), int(cos(b) * cos(g))],
    ]

def dot_product(v1, v2):
    return sum(x*y for x,y in zip(v1,v2))

def mat_mul(m, v):
    return tuple(
        dot_product(row, v) for row in m
    )

def apply_rotation(points, rm):
    return [mat_mul(rm, p) for p in points]


all_rotation_matrices = [
    generate_rotation_matrix_3d(a,b,g)
    for a,b,g in itertools.product(*itertools.repeat([0,1,2,3], 3))
]

unique_rotation_matrices = []

for rm in all_rotation_matrices:
    if rm not in unique_rotation_matrices:
        unique_rotation_matrices.append(rm)

def sub(p1: Tuple[int], p2: Tuple[int]) -> Tuple[int]:
    """Returns p1 - p2"""
    return tuple(x-y for x,y in zip(p1,p2))

def add(p1: Tuple[int], p2: Tuple[int]) -> Tuple[int]:
    """Returns p1 + p2"""
    return tuple(x+y for x,y in zip(p1,p2))

def recentre_on_first(points: List[Tuple[int]]) -> List[Tuple[int]]:
    first_point = points[0]
    return [sub(p, first_point) for p in points]

# order could be different, however if we reorder the points based on furthest
# left, the furtherest down we should get the same order for all the points
# (if they are in the same coordinate system)
# ie ordered by x then y then z
def reorder(points: List[Tuple[int]]) -> List[Tuple[int]]:
    return sorted(points)

def ordered_recentre(points: List[Tuple[int]]) -> List[Tuple[int]]:
    return recentre_on_first(reorder(points))

def shared_points(points1, points2):
    points1 = reorder(points1)
    points2 = reorder(points2)

    # note that the leftmost point might be different for each set of points
    # we can iterate over both sets second set removing an element each time
    points1_subsets = [(set(recentre_on_first(points1[i:])), points1[i]) for i in range(len(points1))]
    points2_subsets = [(set(recentre_on_first(points2[i:])), points2[i]) for i in range(len(points2))]

    # note that the leftmost point might be different for each set of points
    # we can iterate over both sets second set removing an element each time

    shared = [
        (reorder(list(ps1.intersection(ps2))), (bp1, bp2))
        for (ps1, bp1), (ps2, bp2) in itertools.product(points1_subsets, points2_subsets)
    ]

    max_number_shared = max(len(x[0]) for x in shared)
    max_shared_set = list(filter(lambda x: len(x[0])==max_number_shared, shared))[0]

    # we want the relative offset of the origin of set 2, compared to set 1
    # which is o2 - o1
    # we have the relative vectors: (bp1 - o1) and (bp2 - o2) (for the base points bp1 and bp2)
    # therefore our offset is:
    # (bp1 - o1) - (bp2 - o2) = (bp1 - o1 - bp2 + o2)
    # but bp1 and bp2 are the _same_ point
    rel_offset = sub(max_shared_set[1][0], max_shared_set[1][1])

    # add back the base point of one to the shared points, so you get the
    # points relative to the coordinate system of scanner one
    shared_points = [add(max_shared_set[1][0], p) for p in max_shared_set[0]]

    return shared_points, rel_offset

def shared_points_under_rotation(points1, points2, rm):
    points2 = apply_rotation(points2, rm)

    return shared_points(points1, points2)

def scanner_overlap(scanner1, scanner2):
    # we know that scanners overlap when there are 12 shared beacons, so we
    # can exit the loop at that point
    for rm in unique_rotation_matrices:
        shared, rel_offset = shared_points_under_rotation(scanner1, scanner2, rm)
        if len(shared) == 12: break

    return shared, rel_offset, rm

def read_data(filename):
    with open(filename) as f:
        data = [
            [tuple(int(x) for x in row.strip().split(",")) for row in scanner.strip().split("\n")[1:]]
            for scanner in f.read().strip().split("\n\n")
        ]
    return data



scanners = read_data("data-day19.txt")

overlaps = []
all_beacon_locations = scanners[0]
next_to_check = [0]
checked = []

while next_to_check:
    j = next_to_check.pop()
    for i in range(len(scanners)):
        if i == j: continue
        if i in checked: continue

        current_scanner = scanners[i]
        print(f"Check for overlap between scanner {j} and scanner {i}")
        overlap_points, offset, rm = scanner_overlap(scanners[j], current_scanner)
        if len(overlap_points) == 12:
            next_to_check.append(i)
            overlaps.append([(j, i), offset, rm])
            # now we want to transform everything in an overlapping scanner
            # to the coordinates of scanner 0, if we do this iteratively
            # then any scanner that overlaps with 0 will be in zero,
            # so then any scanner that overlaps with it will be etc.
            scanners[i] = [add(mat_mul(rm, p), offset) for p in current_scanner]
            all_beacon_locations.extend(scanners[i])
    checked.append(j)

print(f"There are a total of : {len(set(all_beacon_locations))} beacons")

scanner_locations = [o[1] for o in overlaps]

scanner_distances = [sum(sub(s1, s2)) for s1,s2 in itertools.product(scanner_locations, repeat=2)]

print(f"Max distance between them is: {max(scanner_distances)}")
