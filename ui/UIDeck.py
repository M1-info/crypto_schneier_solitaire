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
        if is_creator:
            texte = "Voici le jeu de cartes qui va servir à chiffrer le message. Nous vous conseillons de le mélanger à l'aide du bouton 'Mélanger' ci-dessous."
        else:
            texte = "Voici le jeu de cartes qui vous a été envoyé et qui va servir à chiffrer le message."
        ttk.Label(self.canvas, text=texte, font=("Helvetica", 10)).grid(row=1, column=0, columnspan=14)
        self.draw_cards()

        if is_creator:
            ttk.Button(self.canvas, text="Mélanger", command=self.shuffle).grid(row=5, column=13, columnspan=2)

    def shuffle(self):
        self.deck.shuffle_deck()
        self.redraw()
    
    def redraw(self):
        for card in self.cards:
            card.canvas.destroy()
        self.draw_cards()
