import day18
import pytest

@pytest.mark.parametrize(
    "example, expected",
    [
        ([[1,2],[[3,4],5]], 143),
        ([[[[0,7],4],[[7,8],[6,0]]],[8,1]], 1384),
        ([[[[1,1],[2,2]],[3,3]],[4,4]], 445),
        ([[[[3,0],[5,3]],[4,4]],[5,5]], 791),
        ([[[[5,0],[7,4]],[5,5]],[6,6]], 1137),
        ([[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]], 3488),
    ]
)
def test_magnitude(example, expected):
    assert day18.magnitude(example) == expected

@pytest.mark.parametrize(
    "example, expected",
    [
        ([1, 2], ([1, 2], False)),
        ([10, 2], ([[5, 5], 2], True)),
        ([[[[0,7],4],[15,[0,13]]],[1,1]], ([[[[0,7],4],[[7,8],[0,13]]],[1,1]], True)),
        ([[[[0,7],4],[[7,8],[0,13]]],[1,1]], ([[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]], True)),
    ]
)
def test_split(example, expected):
    assert day18.split(example) == expected

@pytest.mark.parametrize(
    "example, expected",
    [
        (([1,2], 3), [4,2]),
        (([[1, 1],2], 3), [[4, 1], 2]),
        (([[[1, 1], 1], [2, 2]], 3), [[[4, 1], 1], [2, 2]]),
    ]
)
def test_add_to_leftmost(example, expected):
    assert day18.add_to_leftmost(example[0], example[1]) == expected

@pytest.mark.parametrize(
    "example, expected",
    [
        ([[[[[9,8],1],2],3],4], [[[[0,9],2],3],4]),
        ([7,[6,[5,[4,[3,2]]]]], [7,[6,[5,[7,0]]]]),
        ([[6,[5,[4,[3,2]]]],1], [[6,[5,[7,0]]],3]),
        ([[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]], [[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]),
        ([[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]], [[3,[2,[8,0]]],[9,[5,[7,0]]]]),
        ([[[[0,7],4],[7,[[8,4],9]]],[1,1]], [[[[0,7],4],[15,[0,13]]],[1,1]]),
    ]
)
def test_explode(example, expected):
    assert day18.explode(example)[0] == expected


@pytest.mark.parametrize(
    "example, expected",
    [
        ([[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]], [[[[0,7],4],[[7,8],[6,0]]],[8,1]]),
    ]
)
def test_reduce(example, expected):
    assert day18.reduce(example) == expected

@pytest.mark.parametrize(
    "example, expected",
    [
        (([1,2], [[3,4],5]), [[1,2],[[3,4],5]]),
        (([[[[4,3],4],4],[7,[[8,4],9]]], [1,1]), [[[[0,7],4],[[7,8],[6,0]]],[8,1]]),
        (([[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]], [7,[[[3,7],[4,3]],[[6,3],[8,8]]]]), [[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]])
    ]
)
def test_add(example, expected):
    assert day18.add(example[0], example[1]) == expected

@pytest.mark.parametrize(
    "example, expected",
    [
        ([[1,1], [2,2], [3,3], [4,4]], [[[[1,1],[2,2]],[3,3]],[4,4]]),
        ([[1,1], [2,2], [3,3], [4,4], [5,5]], [[[[3,0],[5,3]],[4,4]],[5,5]]),
        ([[1,1], [2,2], [3,3], [4,4], [5,5], [6,6]], [[[[5,0],[7,4]],[5,5]],[6,6]]),
    ]
)
def test_add_list(example, expected):
    assert day18.add_list(example) == expected

@pytest.mark.parametrize(
    "example, expected",
    [
        ("data-day18-example.txt", [[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]),
        ("data-day18-example2.txt", [[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]),
    ]
)
def test_solve(example, expected):
    assert day18.solve(example) == expected

@pytest.mark.parametrize(
    "example, expected",
    [
        ("data-day18-example2.txt", 3993),
    ]
)
def test_solve(example, expected):
    assert day18.solve_part_two(example) == expected
