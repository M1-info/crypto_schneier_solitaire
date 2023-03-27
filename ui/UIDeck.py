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
        row = 1
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
    def draw(self):
        text ="Jeu de cartes utilisé pour le chiffrement Solitaire. Nous vous conseillons de le mélanger."
        self.draw_label = ttk.Label(self.canvas, text = text, font="Helvetica 10", foreground="black", background="#f0f0f0")
        self.draw_label.grid(row=0, column=0, columnspan=12, pady=10)
        self.draw_cards()


    def shuffle(self):
        self.deck.shuffle_deck()
        self.redraw()
    
    def redraw(self):
        for card in self.cards:
            card.canvas.destroy()
        self.draw_cards()
