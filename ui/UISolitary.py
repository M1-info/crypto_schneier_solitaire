import socket
from typing import Optional
from tkinter import Misc, Canvas, Button, Text
from .UIDeck import UIDeck
from cipher.Deck import Deck

from cipher.Solitary import Solitary

class UISolitary:
    def __init__(self, ui_deck: UIDeck, parent: Optional[Misc] = None):
        self.solitary = Solitary()
        self.ui_deck = ui_deck

        # Create the text box to enter the message
        self.canvas = Canvas(parent, width=100, height=600)

        self.message_input = Text(self.canvas, height=2, width=10)
        self.message_input.grid(row=1, column=1)

        # Create the button to encrypt the message and send it
        self.encrypt_button = Button(self.canvas, text="Encrypt", command=self.encrypt)
        self.encrypt_button.grid(row=1, column=2)

    def encrypt(self):
        message = self.message_input.get("1.0", "end-1c")
        crypted_message = self.solitary.crypt(message, self.ui_deck.deck, True)

    def decrypt(self):
        message = self.message_input.get("1.0", "end-1c")
        decrypted_message = self.solitary.crypt(message, self.ui_deck.deck, False)