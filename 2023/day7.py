import bisect
import enum
import logging
from typing import TextIO, Tuple


class HandType(enum.Enum):
    Kind5 = 6
    Kind4 = 5
    FullHouse = 4
    Kind3 = 3
    TwoPair = 2
    OnePair = 1
    High = 0

    @classmethod
    def from_cards(cls, cards: list[int]) -> "HandType":
        d = {}

        for card in cards:
            if card in d:
                d[card] += 1
            else:
                d[card] = 1

        add = 0
        if 1 in d:
            if d[1] == 5:
                return HandType.Kind5

            add = d[1]
            del d[1]

        num_unique_cards = len(d.keys())
        max_group = max(d.values())

        max_group += add

        if num_unique_cards == 5:
            return HandType.High

        if num_unique_cards == 4:
            return HandType.OnePair

        if num_unique_cards == 1:
            return HandType.Kind5

        if num_unique_cards == 2:
            if max_group == 4:
                return HandType.Kind4
            if max_group == 3:
                return HandType.FullHouse

        if num_unique_cards == 3:
            if max_group == 3:
                return HandType.Kind3
            if max_group == 2:
                return HandType.TwoPair

        print("here")
        print(num_unique_cards, max_group)


class CardType(enum.Enum):
    A = 14
    K = 13
    Q = 12
    J = 1
    T = 10


class Hand:
    def __init__(self, cards: list[int], type: HandType, bid: int) -> None:
        self.cards = cards
        self.type = type
        self.bid = bid

    @classmethod
    def from_string(cls, hand: str, bid: str) -> "Hand":
        cards = []
        for card in hand:
            try:
                cards.append(int(card))
            except ValueError:
                cards.append(CardType[card.upper()].value)

        type = HandType.from_cards(cards)

        return cls(cards, type, int(bid))

    def __lt__(self, other: "Hand") -> bool:
        if self.type.value == other.type.value:
            for this_card, that_card in zip(self.cards, other.cards):
                if this_card == that_card:
                    continue

                return this_card < that_card

        return self.type.value < other.type.value


def run(file: TextIO) -> Tuple[int, int]:
    """Run the solution for this day."""
    part_one, part_two = 0, 0

    hands = []

    for line in file:
        hand, bid = line.strip().split()
        bisect.insort(hands, Hand.from_string(hand, bid))

    part_one = 0
    for rank, hand in enumerate(hands, 1):
        part_one += rank * hand.bid

    return part_one, part_two
