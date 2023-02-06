import random
import itertools
from utils import Logger, ChoseListConsole
import json
from art import text2art


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
    
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)
    
    @staticmethod
    def fromJSON(string: str):
        return json.loads(string, object_hook=lambda d: Card(d['suit'], d['rank'], d['id']))

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
            Card(suit, rank, id) for id, (suit, rank) in enumerate(itertools.product(suits, ranks), start=1)
        ]

        # instance new Card for jokers
        self.cards.append(Card(CardSuit.BLACK_JOKER, CardValue.JOKER, 53))
        self.cards.append(Card(CardSuit.RED_JOKER, CardValue.JOKER, 53))

    # shuffle the deck randomly
    def shuffle(self) -> None:
        random.shuffle(self.cards)

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
    
    # print the deck of cards in the console
    def print_deck(self):
        print("\n" + Logger.Style.bold + text2art("Deck", font="cards") + Logger.reset)
        for i, card in enumerate(self.cards):
            rank = str(card.rank)

            if card.suit == CardSuit.HEARTS :
                print(Logger.Foreground.red + '♥' + rank + Logger.reset, end="")
            elif card.suit == CardSuit.DIAMONDS :
                print(Logger.Foreground.red + '♦' + rank + Logger.reset, end="")
            elif card.suit == CardSuit.CLUBS :
                print('♣' + rank + Logger.reset, end="")
            elif card.suit == CardSuit.SPADES :
                print('♠' + rank + Logger.reset, end="")
            elif card.suit == CardSuit.BLACK_JOKER :
                print(Logger.Foreground.black + '🃏' + Logger.reset, end="")
            elif card.suit == CardSuit.RED_JOKER :
                print(Logger.Background.red + Logger.Foreground.red + '🃏' + Logger.reset, end="")
            
            if i != len(self.cards) - 1:
                print("|", end="")
            else:
                print("\n\n")

    # ask to the user if he want to shuffle the deck
    def ask_to_shuffle(self):
        message = Logger.Style.underline + "Do you want to shuffle the deck 🔀 ?" + Logger.reset
        options = ["👍 Obviously man !", "👎 No, thanks anyway."]
        chose = ChoseListConsole(message, options).chose()

        if options[chose] == options[0]:
            self.shuffle()
            print("\n" + Logger.Background.lightgrey + Logger.Foreground.black + "Deck shuffled" + Logger.reset)
            self.print_deck()
            
            shuffles = 0
            while True:
                print(Logger.separator, end="\n")
                message = Logger.Style.underline + "Do you want to shuffle it again " + ''.join("(again) " for _ in range(shuffles))  + "?" + Logger.reset
                options = ["Let's go 👍", "No, is enough for me. 👎"]
                chose = ChoseListConsole(message, options).chose()
                if options[chose] == options[0]:
                    if shuffles == 3:
                        print("\n" + Logger.Background.red + "You've already shuffled the deck 3 times 🥱, it's enough." + Logger.reset, end="\n")
                        break
                    self.shuffle()
                    print("\n" + Logger.Background.lightgrey + Logger.Foreground.black + "Deck shuffled" + Logger.reset)
                    self.print_deck()
                    shuffles += 1
                else:
                    break

    def serialize(self) -> dict:
        return {
            "cards": [card.toJSON() for card in self.cards]
        }
    
    @classmethod
    def deserialize(self, data) -> 'Deck':
        self.cards = [Card.fromJSON(card) for card in data["cards"]]
        return self
