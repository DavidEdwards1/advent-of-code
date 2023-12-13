from aoc_python_2023 import day03


EXAMPLE = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
"""


def test_part_one():
    assert day03.part_one(EXAMPLE) == 4361


def test_part_two():
    assert day03.part_two(EXAMPLE) == 467835


def test_symbol_neighborhood():
    assert len(day03.Symbol("*", (1, 2)).neighborhood()) == 9


def test_numbers_list():
    assert day03.numbers_list(EXAMPLE) == day03.NumberCollection([
        day03.Number(467, {(0, 0), (0, 1), (0, 2)}),
        day03.Number(114, {(0, 5), (0, 6), (0, 7)}),
        day03.Number(35, {(2, 2), (2, 3)}),
        day03.Number(633, {(2, 6), (2, 7), (2, 8)}),
        day03.Number(617, {(4, 0), (4, 1), (4, 2)}),
        day03.Number(58, {(5, 7), (5, 8)}),
        day03.Number(592, {(6, 2), (6, 3), (6, 4)}),
        day03.Number(755, {(7, 6), (7, 7), (7, 8)}),
        day03.Number(664, {(9, 1), (9, 2), (9, 3)}),
        day03.Number(598, {(9, 5), (9, 6), (9, 7)})
    ])


def test_number_collection_get_item():
    assert (
        day03.numbers_list(EXAMPLE)[0]
        == day03.Number(467, {(0, 0), (0, 1), (0, 2)})
    )
    assert (
        day03.numbers_list(EXAMPLE)[(9, 5)]
        == day03.Number(598, {(9, 5), (9, 6), (9, 7)})
    )


def test_symbols_list():
    assert day03.symbols_list(EXAMPLE) == [
        day03.Symbol("*", (1, 3)),
        day03.Symbol("#", (3, 6)),
        day03.Symbol("*", (4, 3)),
        day03.Symbol("+", (5, 5)),
        day03.Symbol("$", (8, 3)),
        day03.Symbol("*", (8, 5)),
    ]


def test_symbols_adjacent_numbers():
    assert (
        day03.Symbol("*", (1, 3)).adjacent_numbers(day03.numbers_list(EXAMPLE))
        == set(
            [
                day03.Number(467, frozenset([(0, 0), (0, 1), (0, 2)])),
                day03.Number(35, frozenset([(2, 2), (2, 3)])),
            ]
        )
    )
