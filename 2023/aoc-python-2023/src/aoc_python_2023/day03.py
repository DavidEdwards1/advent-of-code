from dataclasses import dataclass
import itertools
import math
from typing import Iterator, Union


@dataclass(frozen=True)
class Number:
    value: int
    positions: frozenset[tuple[int, int]]

    @classmethod
    def from_chars(cls, chars: list[tuple[str, tuple[int, int]]]) -> "Number":
        return Number(
            int("".join(char[0] for char in chars)),
            frozenset(char[1] for char in chars),
        )


@dataclass
class NumberCollection:
    numbers: list[Number]

    def __post_init__(self):
        self.number_dict = {
            pos: num for num in self.numbers for pos in num.positions
        }

    def __getitem__(self, index: Union[int, tuple[int, int]]) -> Number:
        if isinstance(index, int):
            return self.numbers[index]
        else:
            return self.number_dict.get(index)


@dataclass
class Symbol:
    value: str
    position: tuple[int, int]

    def adjacent(self, num: Number) -> bool:
        return len(self.neighborhood().intersection(num.positions)) > 0

    def neighborhood(self) -> set[tuple[int, int]]:
        return {
            (self.position[0]+offset[0], self.position[1]+offset[1])
            for offset in itertools.product([-1, 0, 1], [-1, 0, 1])
        }

    def adjacent_numbers(self, numbers: NumberCollection) -> set[Number]:
        return set(
            numbers[pos] for pos in self.neighborhood()
            if numbers[pos]
        )

    def is_gear(self, numbers: NumberCollection) -> bool:
        return (
            (self.value == "*")
            and (len(self.adjacent_numbers(numbers)) == 2)
        )


def tokens(input: str) -> Iterator[tuple[str, tuple[int, int]]]:
    rows = list(enumerate(input.split("\n")))
    return (
        (el, (row_number, col_number))
        for row_number, row in rows
        for col_number, el in enumerate(list(row))
    )


def symbols_list(input: str) -> list[Symbol]:
    return [
        Symbol(el, pos)
        for (el, pos) in tokens(input)
        if (not el.isnumeric()) and (el != ".")
    ]


def numbers_list(input: str) -> list[Number]:
    return NumberCollection([
        Number.from_chars(list(group[1]))
        for group in itertools.groupby(
            tokens(input),
            key=lambda x: x[0].isnumeric())
        if group[0]
    ])


def part_one(input: str):
    return sum(
        num.value
        for num in numbers_list(input)
        if any(sym.adjacent(num) for sym in symbols_list(input))
    )


def part_two(input: str):
    numbers = numbers_list(input)
    return sum(
        math.prod(num.value for num in sym.adjacent_numbers(numbers))
        for sym in symbols_list(input)
        if sym.is_gear(numbers)
    )


if __name__ == "__main__":
    with open("data/day03.txt", "r", encoding="utf8") as f:
        data = f.read()
        print(f"Part One: {part_one(data)}")
        print(f"Part Two: {part_two(data)}")
