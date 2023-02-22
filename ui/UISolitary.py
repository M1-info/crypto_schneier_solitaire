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

    client_socket: socket.socket
    thread: threading.Thread

    window: tk.Tk
    create_deck_button: ttk.Button
    validate_deck_button: ttk.Button
    is_creator: bool = False
    want_to_close: bool = False

    def __init__(self):

        # self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.client.connect(ADDRESS)
        # self.client.setblocking(False)

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

        # thread = threading.Thread(target=self.listen_to_receive_deck)
        # self.threads.append(thread)
        # thread.start()

        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

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

        # thread = threading.Thread(target=self.listen_to_receive_message)
        # self.threads.append(thread)
        # thread.start()

        self.thread = threading.Thread(target=self.listen_to_receive_message)
        self.thread.start()

    def listen_to_receive_deck(self):
        while True:
            print("Waiting for deck")
            if self.is_creator or self.want_to_close:
                break
            try:
                data = self.client.recv(MAX_DATA_SIZE)
                if data:
                    self.deck_ui = UIDeck(Deck.deserialize(json.loads(data.decode(FORMAT))).cards.copy())
                    self.deck_ui.canvas = tk.Canvas(self.container, width=100, height=600)
                    self.deck_ui.canvas.grid(row=1, column=0, pady=30)
                    self.deck_ui.draw(is_creator=False)

                    self.thread = threading.Thread(target=self.listen_to_receive_message)
                    self.thread.start()

                    break
            except BlockingIOError:
                continue
        
    def listen_to_receive_message(self):
        self.draw_message_box()
        while True:
            if self.want_to_close:
                break
            try:
                data = self.client.recv(MAX_DATA_SIZE)
                if data:
                    print(data.decode(FORMAT))
                    self.received_messages_box.insert(tk.END, data.decode(FORMAT))
            except BlockingIOError:
                continue


    def draw_message_box(self):
        # Create the button to send the message
        self.send_message_button = ttk.Button(self.container, text="Envoyer le message", command=self.send_message)
        self.send_message_button.grid(row=5, column=0)

        # Create the input text to enter the message
        self.message_input = ttk.Entry(self.container, width=100)
        self.message_input.grid(row=5, column=1)

        self.received_messages_box = tk.Text(self.container, width=100, height=10)
        self.received_messages_box.grid(row=6, column=0, columnspan=2)

    def send_message(self):
        message = self.message_input.get().encode(FORMAT)
        self.client.send(message)

    def on_closing(self):
        self.want_to_close = True
        if hasattr(self, "thread"):
            self.thread.join()
        self.client.close()
        self.window.destroy()