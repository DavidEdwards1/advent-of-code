from collections import Counter
from dataclasses import dataclass
from enum import Enum


class HandType(Enum):
    HIGH = 0
    ONE = 1
    TWO = 2
    THREE = 3
    FULL = 4
    FOUR = 5
    FIVE = 6


@dataclass
class Hand:
    bid: int
    cards: str

    ###########################
    # this is the only stuff that changes between part 1 and 2
    card_ranking = "23456789TJQKA"

    def most_common_counts(self) -> list[int]:
        most_common = Counter(self.cards).most_common(2)

        top_two = [
            most_common[0][1],
            most_common[1][1] if len(most_common) > 1 else 0
        ]
        return top_two

    #########################

    def type(self):
        match self.most_common_counts():
            case [5, _]:
                hand_type = HandType.FIVE
            case [4, _]:
                hand_type = HandType.FOUR
            case [3, 2]:
                hand_type = HandType.FULL
            case [3, 1]:
                hand_type = HandType.THREE
            case [2, 2]:
                hand_type = HandType.TWO
            case [2, 1]:
                hand_type = HandType.ONE
            case _:
                hand_type = HandType.HIGH
        return hand_type

    def card_order(self):
        return [self.card_ranking.index(c) for c in self.cards]

    @classmethod
    def from_row(cls, input: str):
        parts = input.strip().split()

        return cls(int(parts[1]), parts[0])


@dataclass
class JokersHand(Hand):
    card_ranking = "J23456789TQKA"

    def most_common_counts(self) -> list[int]:
        counter = Counter(self.cards)

        jokers = counter.pop("J")if "J" in counter else 0

        most_common = counter.most_common(2)

        top_two = [
            most_common[0][1] + jokers if most_common else jokers,
            most_common[1][1] if len(most_common) > 1 else 0
        ]

        return top_two


def part_one(input):
    hands = (Hand.from_row(row) for row in input.strip().split("\n"))

    hands = sorted(
        hands,
        key=lambda hand: (hand.type().value, hand.card_order())
    )

    return sum(
        bid * (rank + 1)
        for rank, bid in enumerate(h.bid for h in hands)
    )


def part_two(input):
    hands = (JokersHand.from_row(row) for row in input.strip().split("\n"))

    hands = sorted(
        hands,
        key=lambda hand: (hand.type().value, hand.card_order())
    )

    return sum(
        bid * (rank + 1)
        for rank, bid in enumerate(h.bid for h in hands)
    )


if __name__ == "__main__":
    with open("data/day07.txt", "r", encoding="utf8") as f:
        data = f.read()
        print(f"Part One: {part_one(data)}")
        print(f"Part Two: {part_two(data)}")
