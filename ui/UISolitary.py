import json
import socket
import threading

import tkinter as tk
import tkinter.ttk as ttk

from .UIDeck import UIDeck
from cipher.Deck import Deck

HEADER = 64
HOST = socket.gethostbyname(socket.gethostname())
PORT = 65432
FORMAT = "utf-8"
ADDRESS = (HOST, PORT)
MAX_DATA_SIZE = 4000


class UISolitary:

    client: socket.socket
    thread: threading.Thread

    window: tk.Tk
    create_deck_button: ttk.Button
    validate_deck_button: ttk.Button
    is_creator: bool = False

    def __init__(self):

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(ADDRESS)

        # Create the main window
        self.window = tk.Tk()
        self.window.title("Chiffrement Solitaire")
        self.window.geometry("900x550")

        # Create the main frame
        self.container = ttk.Frame(self.window, padding=30)
        self.container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Create the title
        font = ("Helvetica", 36, "bold")
        ttk.Label(self.container, text="Chiffrement solitaire", font=font, padding=30).grid(row=0, column=0, columnspan=2)

        # Create the buttons to initiate or wait for a deck
        self.create_deck_button = ttk.Button(self.container, text="Commencer un echange", command=self.on_initiate)
        self.create_deck_button.grid(row=1, column=0)

        self.thread = threading.Thread(target=self.listen_to_receive_deck)
        self.thread.start()

        self.window.mainloop()

    def on_initiate(self):

        # Create the deck view
        self.deck_ui = UIDeck()
        self.deck_ui.canvas = tk.Canvas(self.container, width=100, height=600)
        self.deck_ui.canvas.grid(row=1, column=0, pady=30)
        self.deck_ui.draw()

        # Disable the initiate button and the wait button
        self.create_deck_button.destroy()

        # Create the button to validate the exchange
        self.validate_deck_button = ttk.Button(self.container, text="Valider", command=self.send_deck)
        self.validate_deck_button.grid(row=4, column=0, columnspan=14)

    def send_deck(self):
        self.is_creator = True
        message = json.dumps(self.deck_ui.deck.serialize()).encode(FORMAT)
        self.client.send(message)

    def listen_to_receive_deck(self):
        while True:
            if self.is_creator:
                break
            data = self.client.recv(MAX_DATA_SIZE)
            if data:
                self.deck_ui = UIDeck(Deck.deserialize(json.loads(data.decode(FORMAT))).cards.copy())
                self.deck_ui.canvas = tk.Canvas(self.container, width=100, height=600)
                self.deck_ui.canvas.grid(row=1, column=0, pady=30)
                self.deck_ui.draw(is_creator=False)
                break

        self.client.close()
        