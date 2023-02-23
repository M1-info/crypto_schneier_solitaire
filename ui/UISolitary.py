import json
import tkinter as tk
import tkinter.ttk as ttk
from socket import socket
import selectors
import threading

from .UIDeck import UIDeck
from cipher.Deck import Deck

MAX_DATA_SIZE = 4000
FORMAT = "utf-8"

class UISolitary:
    def __init__(self, socket: socket):
        self.socket = socket
        self.selector = selectors.DefaultSelector()
        self.selector.register(self.socket, selectors.EVENT_READ, self.on_receive_message)
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

        self.window = tk.Tk()
        self.window.title("Chiffrement Solitaire")
        self.window.geometry("900x550")

        self.container = ttk.Frame(self.window, padding=30)
        self.container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        font = ("Helvetica", 36, "bold")
        ttk.Label(self.container, text="Chiffrement solitaire", font=font, padding=30).grid(row=0, column=0, columnspan=2)

        self.create_deck_button = ttk.Button(self.container, text="Créer un jeu de cartes", command=self.on_build_deck)
        self.create_deck_button.grid(row=1, column=0)

        self.window.mainloop()

    def on_build_deck(self):
        self.create_deck_button.grid_forget()
        self.ui_deck = UIDeck()
        self.ui_deck.canvas = ttk.Frame(self.container)
        self.ui_deck.canvas.grid(row=2, column=0)
        self.ui_deck.draw(is_creator=True)
        self.validate_deck_button = ttk.Button(self.container, text="Valider le jeu de cartes", command=self.on_validate_deck)
        self.validate_deck_button.grid(row=2, column=0)

    def on_validate_deck(self):
        self.validate_deck_button.grid_forget()
        self.socket.send(json.dumps({"type": "deck", "deck": self.ui_deck.deck.serialize()}).encode())
        self.draw_message_box()

    def on_receive_deck(self, deck: bytes):
        self.create_deck_button.grid_forget()
        self.ui_deck = UIDeck(Deck.deserialize(deck).cards.copy())
        self.ui_deck.canvas = ttk.Frame(self.container)
        self.ui_deck.canvas.grid(row=2, column=0)
        self.ui_deck.draw(is_creator=False)
        self.draw_message_box()

    def on_receive_message(self, conn: socket, mask: selectors.EVENT_READ):
        message = json.loads(conn.recv(MAX_DATA_SIZE).decode())
        if message["type"] == "deck":
            self.on_receive_deck(message["deck"])
        elif message["type"] == "message":
            self.received_messages_box.insert(tk.END, message["message"])

    def on_send_message(self):
        message = self.message_input.get()
        self.socket.send(json.dumps({"type": "message", "message": message}).encode())

    def draw_message_box(self):
        # Create the button to send the message
        self.send_message_button = ttk.Button(self.container, text="Envoyer le message", command=self.on_send_message)
        self.send_message_button.grid(row=5, column=0)

        # Create the input text to enter the message
        self.message_input = ttk.Entry(self.container, width=100)
        self.message_input.grid(row=5, column=1)

        self.received_messages_box = tk.Text(self.container, width=100, height=10)
        self.received_messages_box.grid(row=6, column=0, columnspan=2)


    def run(self):
        while True:
            events = self.selector.select()
            for key, mask in events:
                callback = key.data
                callback(key.fileobj, mask)

    def on_closing(self):
        self.thread.join()
        self.socket.close()
        self.selector.close()
        self.window.destroy()