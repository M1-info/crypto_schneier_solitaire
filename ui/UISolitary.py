import json
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.scrolledtext as scrolledtext
import socket
import selectors
import threading

from .UIDeck import UIDeck
from cipher.Deck import Deck
from cipher.Solitary import Solitary

HOST = socket.gethostbyname(socket.gethostname())
PORT = 65432
ADDRESS = (HOST, PORT)
MAX_DATA_SIZE = 4000
FORMAT = "utf-8"

class UISolitary:
    def __init__(self):

        self.close_app: bool = False

        self.selector = selectors.DefaultSelector()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(ADDRESS)
        self.socket.setblocking(False)
        self.selector.register(self.socket, selectors.EVENT_READ, self.on_receive_message)
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

        self.cipher = Solitary()

        self.window = tk.Tk()
        self.window.title("Chiffrement Solitaire")
        self.window.geometry("900x550")

        self.container = ttk.Frame(self.window, padding=30)
        self.container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        font = ("Helvetica", 36, "bold")
        ttk.Label(self.container, text="Chiffrement solitaire", font=font, padding=30).grid(row=0, column=0, columnspan=2)

        self.create_deck_button = ttk.Button(self.container, text="Créer un jeu de cartes", command=self.on_build_deck)
        self.create_deck_button.grid(row=1, column=0, columnspan=2)

    def on_build_deck(self):
        self.create_deck_button.grid_forget()
        self.ui_deck = UIDeck()
        self.ui_deck.canvas = ttk.Frame(self.container)
        self.ui_deck.canvas.grid(row=2, column=0, columnspan=2)
        self.ui_deck.draw(is_creator=True)
        self.validate_deck_button = ttk.Button(self.container, text="Valider le jeu de cartes", command=self.on_validate_deck)
        self.validate_deck_button.grid(row=3, column=0, columnspan=2)

    def on_validate_deck(self):
        self.validate_deck_button.grid_forget()
        self.socket.send(json.dumps({"type": "deck", "deck": self.ui_deck.deck.serialize()}).encode())
        self.draw_message_box()

    def on_receive_deck(self, deck: bytes):
        self.create_deck_button.grid_forget()
        self.ui_deck = UIDeck(Deck.deserialize(deck).cards.copy())
        self.ui_deck.canvas = ttk.Frame(self.container)
        self.ui_deck.canvas.grid(row=2, column=0, columnspan=2)
        self.ui_deck.draw(is_creator=False)
        self.draw_message_box()

    def on_receive_message(self, conn: socket.socket, mask: selectors.EVENT_READ):
        try : 
            data = json.loads(conn.recv(MAX_DATA_SIZE).decode())
        except json.decoder.JSONDecodeError:
            return
        if data["type"] == "deck":
            self.on_receive_deck(data["deck"])
        elif data["type"] == "message":
            message = self.cipher.crypt(data["message"], self.ui_deck.deck, is_encrypt=False)
            self.received_messages_box.insert("1.0", message + '\n')

    def on_send_message(self):
        message = self.message_input.get()
        message = self.cipher.crypt(message, self.ui_deck.deck, is_encrypt=True)
        self.socket.send(json.dumps({"type": "message", "message": message}).encode())
        self.message_input.delete(0, tk.END)

    def draw_message_box(self):
        # Create the button to send the message
        self.send_message_button = ttk.Button(self.container, text="Envoyer le message", command=self.on_send_message)
        self.send_message_button.grid(row=3, column=1)

        # Create the input text to enter the message
        self.message_input = ttk.Entry(self.container, width=100)
        self.message_input.grid(row=3, column=0)

        self.received_messages_box = scrolledtext.ScrolledText(self.container, width=100, height=10)
        self.received_messages_box.grid(row=4, column=0, columnspan=2)

    def run(self):
        while not self.close_app:
            events = self.selector.select(timeout=0)
            for key, mask in events:
                callback = key.data
                callback(key.fileobj, mask)

    def on_closing(self):
        self.thread.join()
        self.selector.unregister(self.socket)
        self.socket.close()
        self.selector.close()