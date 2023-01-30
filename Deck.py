import random

class Card:
    def __init__(self, suit, rank, id):
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

    def build(self):
        suits = ["Spades", "Clubs", "Diamonds", "Hearts"]
        ranks = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
        self.cards = [Card(suit, rank, id) for suit in suits for rank in ranks for id in range(1, 53)]

        # instance new Card for jokers
        self.cards.append(Card("Red", 0, 53))
        self.cards.append(Card("Black", 0, 54))


    def shuffle(self):
        random.shuffle(self.cards)

    def get_card_index(self, card):
        return self.cards.index(card)

    def get_card_id_by_index(self, index):
        return self.cards[index].id

    def get_joker_index(self, color = "Red"):
        for card in self.cards:
            if card.suit == color:
                return self.cards.index(card)
        return -1

    def get_sub_deck(self, _from=0, _to=-1):
        return self.cards[_from:_to]

    def switch_cards(self, index1, index2):
        self.cards[index1], self.cards[index2] = self.cards[index2], self.cards[index1]

    def switch_sub_deck(self, first_index, second_index):
        first_cards = self.cards[:first_index]
        second_cards = self.cards[second_index+1:]
        self.cards = first_cards + self.cards[first_index:second_index+1] + second_cards

    def is_last_card(self, index):
        return index == len(self.cards) -1

    def is_joker(self, index):
        return self.cards[index].rank == 0

    def move_last_to_front(self):
        self.cards.insert(0, self.cards.pop())

    def print_deck(self):
        for card in self.cards:
            card.print_card()



