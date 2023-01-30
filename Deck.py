import random

import Card

class Deck:
    def __init__(self):
        self.cards = []
        self.original_cards = []
        self.build()

    def build(self):
        suits = ["Spades", "Clubs", "Diamonds", "Hearts"]
        ranks = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
        self.cards = [Card(suit, rank, id) for suit in suits for rank in ranks for id in range(1, 53)]
        
        self.cards.append(Card("Red", 0, 53))
        self.cards.append(Card("Black", 0, 54))

    def shuffle(self):
        random.shuffle(self.cards)
        self.original_cards = self.cards.copy()

    def get_card_index(self, card):
        return self.cards.index(card)

    def switch_cards(self, index1, index2):
        self.cards[index1], self.cards[index2] = self.cards[index2], self.cards[index1]

    def switch_sub_deck(self, first_index, second_index):
        first_cards = self.cards[:first_index]
        second_cards = self.cards[second_index+1:]
        self.cards = first_cards + self.cards[first_index:second_index+1] + second_cards

    