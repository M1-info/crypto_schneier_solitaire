import random
import itertools


class CardSuit:
    SPADES = "Spades"
    CLUBS = "Clubs"
    DIAMONDS = "Diamonds"
    HEARTS = "Hearts"
    RED_JOKER = "Red Joker"
    BLACK_JOKER = "Black Joker"


class CardValue:
    JOKER = 0
    ACE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13


class Card:
    def __init__(self, suit: CardSuit, rank: CardValue, id: int):
        self.suit = suit
        self.rank = rank
        self.id = id
        self.picture = None

    def print_card(self):
        print(self.suit, self.rank, self.id)


class Deck:
    def __init__(self, cards=None):
        if cards is None:
            cards = []
        self.cards = cards

    # build the deck of 54 cards (52 cards + 2 jokers)
    def build(self):
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
            Card(suit, rank, id) for id, (suit, rank) in enumerate(itertools.product(suits, ranks), start=1)
        ]

        # instance new Card for jokers
        self.cards.append(Card(CardSuit.RED_JOKER, CardValue.JOKER, 53))
        self.cards.append(Card(CardSuit.BLACK_JOKER, CardValue.JOKER, 54))

    # shuffle the deck randomly
    def shuffle(self):
        random.shuffle(self.cards)

    # get the index of a card
    # card: Card object
    def index_of(self, card: Card):
        return self.cards.index(card)

    # get the joker index by color
    # color: Red or Black
    def index_of_joker(self, joker_color: CardSuit.BLACK_JOKER or CardSuit.RED_JOKER):
        for index, card in enumerate(self.cards):
            if card.suit == joker_color:
                return index

    # return True if the index is the last card in the deck
    def is_last_card(self, index: int):
        return index == len(self.cards) - 1

    # get the id of a card by index
    def get_card_id_by_index(self, index: int):
        return self.cards[index].id

    # get a sub deck of cards
    # _from: index of the first card
    # _to: index of the last card
    def get_sub_deck(self, _from: int = 0, _to: int = -1):
        if _to > len(self.cards) or _from > len(self.cards) or _from < 0:
            return Exception("Index out of range")
        return self.cards[_from:_to]

    # switch two cards by index in the deck
    # index1: index of the first card
    # index2: index of the second card
    def switch_cards(self, index1: int, index2: int):
        self.cards[index1], self.cards[index2] = self.cards[index2], self.cards[index1]

    # switch two sub deck of cards
    # first_index: index of the first card (the first card of the first sub deck)
    # second_index: index of the second card (the last card of the second sub deck)
    def switch_sub_deck(self, first_index: int, second_index: int):
        first_cards = self.cards[:first_index]
        second_cards = self.cards[second_index+1:]
        self.cards = first_cards + \
            self.cards[first_index:second_index+1] + second_cards

    # return true if the card at the given index is a joker
    # index: index of the card (0-53)
    def is_joker(self, index: int):
        if index == len(self.cards):
            return self.cards[0].rank == CardValue.JOKER
        return self.cards[index].rank == CardValue.JOKER

    # move the last card to the front of the deck
    def move_last_to_front(self):
        self.cards.insert(0, self.cards.pop())

    def print_deck(self):
        for card in self.cards:
            card.print_card()
