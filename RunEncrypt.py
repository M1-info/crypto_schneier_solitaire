import tkinter as tk
import tkinter.ttk as ttk

from cipher.Deck import Deck
from ui.UIDeck import UIDeck
from ui.UISolitary import UISolitary

def main():

    # Create the main window
    root = tk.Tk()
    root.title("Run Encrypt")

    # Create the main frame
    container = ttk.Frame(root, padding=30)
    container.grid(row=1, column=1)

    # Create the title
    title = ttk.Label(container, text="Run Encrypt", font=("Helvetica", 36), padding=30).grid(row=1, column=1)

    # Create the deck view
    deck = Deck()
    deck.build()
    deck_ui = UIDeck(deck, container)
    deck_ui.canvas.grid(row=2, column=1, pady=30)

    # Create the solitary view
    solitary_ui = UISolitary(deck_ui, container)
    solitary_ui.canvas.grid(row=3, column=1)

    root.mainloop()

if __name__ == '__main__':
    main()
