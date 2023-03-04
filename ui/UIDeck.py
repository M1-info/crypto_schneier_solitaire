import tkinter as tk
import tkinter.ttk as ttk

from .UICard import UICard

from cipher.Deck import Deck

class UIDeck :

    deck : Deck
    cards : list[UICard]
    canvas : tk.Canvas

    def __init__(self, cards: list = None):
        self.deck = Deck(cards)
        
        if len(self.deck.cards) == 0:
            self.deck.build()

    def draw_cards(self):
        self.cards = []
        row = 2
        column = 1
        for card in self.deck.cards:
            ui_card = UICard(card, parent=self.canvas)
            ui_card.canvas.grid(row=row, column=column)
            self.cards.append(ui_card)

            if column % 14 == 0:
                row += 1
                column = 0

            column += 1

    # draw the deck
    # if is_creator is True, the deck is drawn with a shuffle button
    def draw(self, is_creator: bool = True):
        texte ="Jeu de cartes utilisé pour le chiffrement Solitaire. Nous vous conseillons de le mélanger."
        self.draw_label = ttk.Label(self.canvas, text = texte, font=("Helvetica", 10))
        self.draw_label.grid(row=1, column=0, columnspan=14)
        self.draw_cards()

        if is_creator:
            self.shuffle_button = ttk.Button(self.canvas, text="Mélanger", command=self.shuffle)
            self.shuffle_button.grid(row=5, column=13, columnspan=2)

    def shuffle(self):
        self.deck.shuffle_deck()
        self.redraw()
    
    def redraw(self):
        for card in self.cards:
            card.canvas.destroy()
        self.draw_cards()
