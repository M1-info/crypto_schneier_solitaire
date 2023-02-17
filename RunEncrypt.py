import tkinter as tk
import tkinter.ttk as ttk
from cipher.Deck import Deck
from ui.UIDeck import UIDeck

def main():

    # Create the main window
    root = tk.Tk()
    root.title("Run Encrypt")

    # Create the main frame
    frame = ttk.Frame(root, padding=30)
    frame.grid(row=2, column=1)

    # Create the title
    title = ttk.Label(frame, text="Run Encrypt", font=("Helvetica", 24)).grid(row=1, column=1)

    # Create the deck view
    deck = Deck()
    deck.build()
    deck_ui = UIDeck(deck, frame)

    root.mainloop()

if __name__ == '__main__':
    main()
