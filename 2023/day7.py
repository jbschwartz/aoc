import bisect
import enum
from functools import cached_property
from typing import TextIO, Tuple


def _replace_jokers(occurances: dict) -> dict:
    if CardType.JOKER.value not in occurances or len(occurances) == 1:
        return occurances

    num_jokers = occurances[CardType.JOKER.value]
    del occurances[CardType.JOKER.value]

    max_card_value = max(occurances, key=occurances.get)
    occurances[max_card_value] += num_jokers

    return occurances


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
        occurances = {}

        # Sum the occurance of each card in the hand.
        for card in cards:
            try:
                occurances[card] += 1
            except KeyError:
                occurances[card] = 1

        occurances = _replace_jokers(occurances)

        largest_group_size = max(occurances.values())

        # See how many unique cards there are in the hand.
        match len(occurances.keys()):
            case 5:
                return HandType.High

            case 4:
                return HandType.OnePair

            case 3:
                if largest_group_size == 3:
                    return HandType.Kind3
                if largest_group_size == 2:
                    return HandType.TwoPair

            case 2:
                if largest_group_size == 4:
                    return HandType.Kind4
                if largest_group_size == 3:
                    return HandType.FullHouse

            case 1:
                return HandType.Kind5


class CardType(enum.Enum):
    A = 14
    K = 13
    Q = 12
    J = 11
    T = 10
    JOKER = 1


class Hand:
    """A hand consists of five card values and a bid."""

    def __init__(self, cards: list[int], bid: int) -> None:
        self.cards = cards
        self.bid = bid

    @classmethod
    def from_string(cls, hand: str, bid: str, use_jokers: bool = False) -> "Hand":
        cards = []
        for card in hand:
            try:
                cards.append(int(card))
            except ValueError:
                card = CardType[card.upper()]
                if card is CardType.J and use_jokers:
                    cards.append(CardType.JOKER.value)
                else:
                    cards.append(card.value)

        return cls(cards, int(bid))

    @cached_property
    def hand_type(self) -> HandType:
        """Get the hand's type."""
        return HandType.from_cards(self.cards)

    def __lt__(self, other: "Hand") -> bool:
        """Compare hands based on the type and then on each individual value."""
        if self.hand_type.value == other.hand_type.value:
            for this_card, that_card in zip(self.cards, other.cards):
                if this_card == that_card:
                    continue

                return this_card < that_card

        return self.hand_type.value < other.hand_type.value


def get_result(file: TextIO, use_jokers: bool = False) -> list[Hand]:
    """Get the result based on whether or not jokers are in play."""
    result = 0
    hands = []

    for line in file:
        hand, bid = line.strip().split()
        bisect.insort(hands, Hand.from_string(hand, bid, use_jokers))

    for rank, hand in enumerate(hands, 1):
        result += rank * hand.bid

    return result


def one(file: TextIO) -> int:
    """Run the first part for this day."""
    return get_result(file)


def two(file: TextIO) -> int:
    """Run the second part for this day."""
    return get_result(file, True)
