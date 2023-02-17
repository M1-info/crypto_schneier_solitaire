from typing import Optional
from tkinter import Misc, Canvas, Button
from cipher.Deck import Deck
from .UICard import UICard

class UIDeck :

    def __init__(self, deck: Deck, parent: Optional[Misc] = None):
        self.deck = deck

        # Create the canvas
        self.canvas = Canvas(parent, width=600, height=600)
        self.canvas.grid(row=2, column=1)
        self.cards = self.init_cards()

        self.button = Button(parent, text="Shuffle", command=self.shuffle)
        self.button.grid(row=6, column=1)

    def init_cards(self):
        cards = []
        row = 1
        column = 1
        for card in self.deck.cards:
            ui_card = UICard(card, parent=self.canvas)
            ui_card.canvas.grid(row=row, column=column)
            cards.append(ui_card)

            if column % 13 == 0:
                row += 1
                column = 0

            column += 1

        return cards

    def shuffle(self):
        self.deck.shuffle_deck()
        self.redraw()
    
    def redraw(self):
        for card in self.cards:
            card.canvas.destroy()
        self.cards = self.init_cards()