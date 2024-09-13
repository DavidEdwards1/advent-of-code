import pytest

import day22
from day22 import Cuboid, Point

@pytest.mark.parametrize(
    "example, expected",
    [
        (
            [Cuboid(Point(10,10,10), Point(13, 13, 13)), Cuboid(Point(11,11,11), Point(14, 14, 14))],
            [Cuboid(Point(11,11,11), Point(13, 13, 13))]
        ),
        (
            [Cuboid(Point(10,10,10), Point(13, 13, 13)), Cuboid(Point(14,14,14), Point(15, 15, 15))],
            []
        ),
        (
            [Cuboid(Point(10,10,10), Point(13, 13, 13)),],
            [Cuboid(Point(10,10,10), Point(13, 13, 13))]
        ),
        (
            [Cuboid(Point(10,10,10), Point(13, 13, 13)), Cuboid(Point(11,11,11), Point(14, 14, 14)), Cuboid(Point(11,11,11), Point(12, 12, 12))],
            [Cuboid(Point(11,11,11), Point(12, 12, 12))]
        ),
        (
            [Cuboid(Point(10,10,10), Point(13, 13, 13)), Cuboid(Point(11,11,11), Point(14, 14, 14)), Cuboid(Point(9,9,9), Point(12, 12, 12), False)],
            [Cuboid(Point(11,11,11), Point(12, 12, 12))]
        ),
        (
            [Cuboid(Point(10,10,10), Point(13, 13, 13)), Cuboid(Point(10,10,10), Point(13, 13, 13)),],
            [Cuboid(Point(10,10,10), Point(13, 13, 13))]
        ),
    ]
)
def test_intersection(example, expected):
    result = day22.intersection(example)
    assert result == expected

@pytest.mark.parametrize(
    "example, expected",
    [
        (
            [Cuboid(Point(10,10,10), Point(13, 13, 13)),],
            27
        ),
        (
            [Cuboid(Point(10,10,10), Point(13, 13, 13)), Cuboid(Point(11,11,11), Point(14, 14, 14))],
            46
        ),
        (
            [
                Cuboid(Point(10,10,10), Point(13, 13, 13)),
                Cuboid(Point(11,11,11), Point(14, 14, 14)),
                Cuboid(Point(0,0,0), Point(3, 3, 3))
            ],
            73
        ),
        (
            [
                Cuboid(Point(10,10,10), Point(13, 13, 13)),
                Cuboid(Point(11,11,11), Point(14, 14, 14)),
                Cuboid(Point(9,9,9), Point(12, 12, 12), False)
            ],
            38
        ),
        (
            [
                Cuboid(Point(9,9,9), Point(12, 12, 12), False),
                Cuboid(Point(10,10,10), Point(11, 11, 11)),
                Cuboid(Point(10,10,10), Point(11, 11, 11), False),
            ],
            0
        ),
        (
            [
                Cuboid(Point(9,9,9), Point(12, 12, 12), False),
                Cuboid(Point(10,10,10), Point(11, 11, 11)),
            ],
            1
        ),
        (
            [
                Cuboid(Point(10,10,10), Point(13, 13, 13)),
                Cuboid(Point(11,11,11), Point(14, 14, 14)),
                Cuboid(Point(9,9,9), Point(12, 12, 12), False),
                Cuboid(Point(10,10,10), Point(11, 11, 11)),
            ],
            39
        ),
    ]
)
def test_inclusion_exclusion(example, expected):
    result = day22.inclusion_exclusion(example)
    assert result == expected
