import json

class CardSuit:
    SPADES = "Spades"
    CLUBS = "Clubs"
    DIAMONDS = "Diamonds"
    HEARTS = "Hearts"
    RED_JOKER = "Red-Joker"
    BLACK_JOKER = "Black-Joker"


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
    
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)
    
    @staticmethod
    def fromJSON(string: str):
        return json.loads(string, object_hook=lambda d: Card(d['suit'], d['rank'], d['id']))