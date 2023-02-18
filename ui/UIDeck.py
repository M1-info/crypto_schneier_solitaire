from tkinter import Canvas
import tkinter.ttk as ttk
from cipher.Deck import Deck
from .UICard import UICard

class UIDeck :

    deck : Deck
    cards : list[UICard]
    canvas : Canvas

    def __init__(self):
        self.deck = Deck()
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

    def draw(self):
        texte = "Voici le jeu de cartes qui va servir à chiffrer le message. Nous vous conseillons de le mélange à l'aide du bouton Shuffle ci-dessous."
        ttk.Label(self.canvas, text=texte, font=("Helvetica", 10)).grid(row=1, column=0, columnspan=14)
        self.draw_cards()
        ttk.Button(self.canvas, text="Shuffle deck", command=self.shuffle).grid(row=5, column=13, columnspan=2)

    def shuffle(self):
        self.deck.shuffle_deck()
        self.redraw()
    
    def redraw(self):
        for card in self.cards:
            card.canvas.destroy()
        self.draw_cards()
