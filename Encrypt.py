import tkinter as tk
import tkinter.ttk as ttk

from cipher.Deck import Deck
from ui.UIDeck import UIDeck
from ui.UISolitary import UISolitary

class Encrypt:

    def __init__(self):
        self.deck = Deck()
        self.deck.build()

    def run(self):
        # Create the main window
        root = tk.Tk()
        root.title("Run Encrypt")
        root.geometry("900x550")

        # Create the main frame
        container = ttk.Frame(root, padding=30)
        container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Create the title
        title = ttk.Label(container, text="Run Encrypt", font=("Helvetica", 36, "bold"), padding=30).grid(row=1, column=1)

        # Create the deck view
        deck = Deck()
        deck.build()
        deck_ui = UIDeck(deck, container)
        deck_ui.canvas.grid(row=2, column=1, pady=30)

        # Create the solitary view
        solitary_ui = UISolitary(deck_ui, container)
        solitary_ui.canvas.grid(row=3, column=1)

        root.mainloop()
        