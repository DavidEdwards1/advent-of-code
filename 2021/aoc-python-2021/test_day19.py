import math
import day19

import pytest

@pytest.mark.parametrize(
    "example, expected",
    [
        ([(1, 2), (0, 0)], (1, 2)), # 2d identity
        ([(1, 2, 3), (0, 0, 0)], (1, 2, 3)), # 3d identity
        ([(0, 2), (-1, -1)], (-1, 1)),
        ([(0, 2, 4), (-1, -1, 7)], (-1, 1, 11))
    ]
)
def test_add(example, expected):
    assert day19.add(example[0], example[1]) == expected

@pytest.mark.parametrize(
    "example, expected",
    [
        ([(1, 2), (0, 0)], (1, 2)), # 2d identity
        ([(1, 2, 3), (0, 0, 0)], (1, 2, 3)), # 3d identity
        ([(0, 2), (-1, -1)], (1, 3)),
        ([(0, 2, 4), (-1, -1, 7)], (1, 3, -3))
    ]
)
def test_sub(example, expected):
    assert day19.sub(example[0], example[1]) == expected

@pytest.mark.parametrize(
    "example, expected",
    [
        ([(0, 2), (4, 1), (3, 3)], [(0,0), (4,-1), (3,1)]),
        ([(-1, -1), (-5, 0), (-2, 1)], [(0, 0), (-4, 1), (-1, 2)]),
    ]
)
def test_recentre_on_first(example, expected):
    assert day19.recentre_on_first(example) == expected

@pytest.mark.parametrize(
    "example, expected",
    [
        ([(0, 2), (4, 1), (3, 3)], [(0, 2), (3, 3), (4, 1)]),
        ([(-1, -1), (-5, 0), (-2, 1)], [(-5, 0), (-2, 1), (-1, -1)]),
    ]
)
def test_reorder(example, expected):
    assert day19.reorder(example) == expected

@pytest.mark.parametrize(
    "example, expected",
    [
        ([(0, 2), (4, 1), (3, 3)], [(0,0), (3,1), (4,-1)]),
        ([(-1, -1), (-5, 0), (-2, 1)], [(0, 0), (3, 1), (4, -1)]),
        ([(-1, -1), (-5, 0), (-2, 1), (-6, 0)], [(0, 0), (1, 0), (4, 1), (5, -1)]),
    ]
)
def test_ordered_recentre(example, expected):
    assert day19.ordered_recentre(example) == expected

@pytest.mark.parametrize(
    "example, expected",
    [
        (([(0, 2), (4, 1), (3, 3)], [(-1, -1), (-5, 0), (-2, 1)]), ([(0,2), (3,3), (4,1)], (5, 2))),
        (([(0, 2), (4, 1), (3, 3)], [(-1, -1), (-5, 0), (-2, 1), (-6, 0)]), ([(0,2), (3,3), (4,1)], (5, 2))),
    ]
)
def test_shared_points(example, expected):
    assert day19.shared_points(example[0], example[1]) == expected

@pytest.mark.parametrize(
    "example, expected",
    [
        ((0,0,0), [[1,0,0],[0,1,0],[0,0,1]]),
        ((1, 0, 0), [[0,-1,0],[1,0,0],[0,0,1]]),
        ((3, 0, 0), [[0,1,0],[-1,0,0],[0,0,1]]),
    ]
)
def test_generate_rotation_matrix_3d(example, expected):
    assert day19.generate_rotation_matrix_3d(*example) == expected

@pytest.mark.parametrize(
    "example, expected",
    [
        (([[1,0,0],[0,1,0],[0,0,1]], (1, 2, 3)), (1,2,3)),
        (([[0,-1,0],[1,0,0],[0,0,1]], (1, 2, 3)), (-2,1,3)),
    ]
)
def test_mat_mul(example, expected):
    assert day19.mat_mul(example[0], example[1]) == expected

@pytest.mark.parametrize(
    "example, expected",
    [
        ((
            [[-1,-1,1], [-2,-2,2], [-3,-3,3], [-2,-3,1], [5,6,-4],  [8,0,7],],
            [[1,-1,1],  [2,-2,2],  [3,-3,3],  [2,-1,3],  [-5,4,-6], [-8,-7,0],],
            [[-1,0,0],[0,0,-1],[0,-1,0]]
        ), (6, [0, 0, 0])),
        ((
            [[-1,-1,1], [-2,-2,2], [-3,-3,3], [-2,-3,1], [5,6,-4],  [8,0,7],],
            [[1,1,-1], [2,2,-2], [3,3,-3], [1,3,-2], [-4,-6,5], [7,0,8],],
            [[0,0,1],[0,-1,0],[1,0,0]]
        ), (6, [0, 0, 0])),
        ((
            [[-618,-824,-621], [-537,-823,-458], [-447,-329,318], [404,-588,-901], [544,-627,-890], [528,-643,409], [-661,-816,-575], [390,-675,-793], [423,-701,434], [-345,-311,381], [459,-707,401], [-485,-357,347]],
            [[686,422,578], [605,423,415], [515,917,-361], [-336,658,858], [-476,619,847], [-460,603,-452], [729,430,532], [-322,571,750], [-355,545,-477], [413,935,-424], [-391,539,-444], [553,889,-390]],
            [[-1,0,0],[0,1,0],[0,0,-1]],
        ), (12, [68,-1246,-43])),
        (( # same as above but with extra point further to the left in set 2
            [[-618,-824,-621], [-537,-823,-458], [-447,-329,318], [404,-588,-901], [544,-627,-890], [528,-643,409], [-661,-816,-575], [390,-675,-793], [423,-701,434], [-345,-311,381], [459,-707,401], [-485,-357,347]],
            [[686,422,578], [605,423,415], [515,917,-361], [-336,658,858], [-476,619,847], [-460,603,-452], [729,430,532], [-322,571,750], [-355,545,-477], [413,935,-424], [-391,539,-444], [553,889,-390], [1100, 0, 0]],
            [[-1,0,0],[0,1,0],[0,0,-1]],
        ), (12, [68,-1246,-43]))
    ]
)
def shared_points_under_rotation(example, expected):
    points1, points2, rm = example
    shared_points, rel_offset = day19.shared_points_under_rotation(points1, points2, rm)
    assert len(shared_points) == expected[0]
    assert rel_offset == expected[1]

@pytest.mark.parametrize(
    "example,expected",
    [
        ((0, 1), (12, (68,-1246,-43), [[-1,0,0],[0,1,0],[0,0,-1]])),
        # for these examples, the order is swapped so relative offset has sign swapped, and you must transform
        # to the coordinate system of the second example
        # the transformation matrix becomes the inverse
        ((1, 0), (12, day19.mat_mul([[-1,0,0],[0,1,0],[0,0,-1]], (-68,1246,43)), [[-1,0,0],[0,1,0],[0,0,-1]])),
        ((1, 4), (12, (88, 113, -1104), [[0,1,0],[0,0,-1],[-1,0,0]])),
        ((4, 1), (12, day19.mat_mul([[0,0,-1],[1,0,0],[0,-1,0]], (-88,-113,1104)), [[0,0,-1],[1,0,0],[0,-1,0]])),
    ]
)
def test_scanner_overlap(example, expected):
    data = day19.read_data("data-day19-example.txt")

    actual_shared, actual_rel_offset, actual_rm = day19.scanner_overlap(data[example[0]], data[example[1]])
    assert len(actual_shared) == expected[0]
    assert actual_rel_offset == expected[1]
    assert actual_rm == expected[2]
