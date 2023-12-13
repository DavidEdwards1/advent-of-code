from aoc_python_2023 import day07


EXAMPLE = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
"""


def test_part_one():
    assert day07.part_one(EXAMPLE) == 6440


def test_part_two():
    assert day07.part_two(EXAMPLE) == 5905


def test_hand_type():
    assert day07.Hand(123, "AAAAA").type() == day07.HandType.FIVE
    assert day07.Hand(123, "AAAQQ").type() == day07.HandType.FULL
    assert day07.Hand(123, "QQT66").type() == day07.HandType.TWO


def test_hand_card_order():
    assert day07.Hand(123, "AAAAA").card_order() == [12, 12, 12, 12, 12]


def test_hand_type_ordering():
    assert day07.HandType.FIVE.value > day07.HandType.THREE.value


def test_jokers_hand_type():
    assert day07.JokersHand(123, "AAJJA").type() == day07.HandType.FIVE
    assert day07.JokersHand(123, "AAJQQ").type() == day07.HandType.FULL
    assert day07.JokersHand(123, "QQTJ6").type() == day07.HandType.THREE
