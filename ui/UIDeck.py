from typing import Optional
from tkinter import Misc, Canvas, Button
from cipher.Deck import Deck
from .UICard import UICard

class UIDeck :

    def __init__(self, deck: Deck, parent: Optional[Misc] = None):
        self.deck = deck

        # Create the canvas
        self.canvas = Canvas(parent, width=600, height=600)

        self.shuffle_button = Button(self.canvas, text="Shuffle deck", command=self.shuffle, bg="seashell4", fg="white", width=15, height=2)
        self.shuffle_button.grid(row=5, column=13, columnspan=2)

        self.cards = self.init_cards()


    def init_cards(self):
        cards = []
        row = 2
        column = 1
        for card in self.deck.cards:
            ui_card = UICard(card, parent=self.canvas)
            ui_card.canvas.grid(row=row, column=column)
            cards.append(ui_card)

            if column % 14 == 0:
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