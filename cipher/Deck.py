from random import shuffle
from itertools import product
from unidecode import unidecode

from .Card import Card, CardSuit, CardValue

class Deck:
    def __init__(self, cards=None):
        if cards is None:
            cards = []
        self.cards = cards

    # build the deck of 54 cards (52 cards + 2 jokers)
    def build(self) -> None:
        suits = [
            CardSuit.CLUBS,
            CardSuit.DIAMONDS,
            CardSuit.HEARTS,
            CardSuit.SPADES
        ]

        ranks = [
            CardValue.ACE,
            CardValue.TWO,
            CardValue.THREE,
            CardValue.FOUR,
            CardValue.FIVE,
            CardValue.SIX,
            CardValue.SEVEN,
            CardValue.EIGHT,
            CardValue.NINE,
            CardValue.TEN,
            CardValue.JACK,
            CardValue.QUEEN,
            CardValue.KING
        ]

        self.cards = [
            Card(suit, rank, id) for id, (suit, rank) in enumerate(product(suits, ranks), start=1)
        ]

        # instance new Card for jokers
        self.cards.append(Card(CardSuit.BLACK_JOKER, CardValue.JOKER, 53))
        self.cards.append(Card(CardSuit.RED_JOKER, CardValue.JOKER, 53))

    # shuffle the deck randomly
    def shuffle_deck(self) -> None:
        shuffle(self.cards)

    # get the joker index by color
    def index_of_joker(self, joker_color: CardSuit.BLACK_JOKER or CardSuit.RED_JOKER) -> int:
        for index, card in enumerate(self.cards):
            if card.suit == joker_color:
                return index

    # get the id of a card by index
    def get_card_id_by_index(self, index: int) -> int:
        return self.cards[index].id

    # get a sub deck of cards
    # _from: index of the first card
    # _to: index of the last card
    def get_sub_deck(self, _from: int = 0, _to: int = -1) -> list:
        if _to > len(self.cards) or _from > len(self.cards) or _from < 0:
            return Exception("Index out of range")
        return self.cards[_from:_to]

    # switch two cards by index in the deck
    # index1: index of the first card
    # index2: index of the second card
    def switch_cards(self, index1: int, index2: int) -> None:
        self.cards[index1], self.cards[index2] = self.cards[index2], self.cards[index1]

    # switch two sub deck of cards
    # first_index: index of the first card (the first card of the first sub deck)
    # second_index: index of the second card (the last card of the second sub deck)

    def switch_sub_deck(self, first_index: int, second_index: int) -> None:
        first_cards = self.cards[:first_index]
        last_cards = self.cards[second_index + 1:]
        middle_cards = self.cards[first_index:second_index + 1]
        self.cards = last_cards + middle_cards + first_cards

    # return true if the card at the given index is a joker
    # index: index of the card (0-53)
    def is_joker(self, index: int) -> bool:
        return self.cards[index].rank == CardValue.JOKER

    def serialize(self) -> dict:
        return {
            "cards": [card.toJSON() for card in self.cards]
        }
    
    @classmethod
    def deserialize(self, data) -> 'Deck':
        self.cards = [Card.fromJSON(card) for card in data["cards"]]
        return self