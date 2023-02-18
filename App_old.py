import json
import socket
import tkinter as tk
import tkinter.ttk as ttk

from cipher.Deck import Deck
from ui.UIDeck import UIDeck

from multiprocessing import Process

from ui.UISolitary import UISolitary

class App:

    def __init__(self) -> None:
        self.deck = None
        # get host and port from config file conf.json
        with open("conf.json", "r") as f:
            conf = json.load(f)
            self.host = conf["host"]
            self.port = conf["port"]
            self.data_size = conf["data_size"]

    def initiate_exchange(self):
        self.deck = Deck()
        self.deck.build()

        # Create the deck view
        deck_ui = UIDeck(self.deck, self.container)
        deck_ui.canvas.grid(row=2, column=1, pady=30)

        # Button to validate the deck
        self.validate_button = ttk.Button(self.container, text="Validate deck", command=self.validate_deck, style="W.TButton")
        self.validate_button.grid(row=5, column=3)

    def validate_deck(self):
        # send the deck to the other app
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((self.host, self.port))
            # send the deck to the other app
            sock.sendall(json.dumps(self.deck.serialize()).encode())
            sock.close()

    def listen_other_app(self):
        print("enter function listen_other_app")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind((self.host, self.port))
            sock.listen()
            connection, _ = sock.accept()
            with connection:
                while True:
                    # wait for the deck
                    print("Waiting for the deck")
                    data = connection.recv(self.data_size)
                    if data:
                        self.deck = Deck(Deck.deserialize(json.loads(data.decode())).cards.copy())
                        print(self.deck)
                        self.processListen.terminate()
                        break

def main():
    app = App()
    
    # Create the main window
    root = tk.Tk()
    root.title("Run cipher")
    root.geometry("900x550")

    # Create the main frame
    app.container = ttk.Frame(root, padding=30)
    app.container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    # Create the title
    title = ttk.Label(app.container, text="Run cipher", font=("Helvetica", 36, "bold"), padding=30).grid(row=1, column=1)

    # Use multithreading to listen for the other app and to be able to send the deck
    Process(target=app.listen_other_app).start()


    # Button to initiate the exchange
    style_button_initiate = ttk.Style()
    style_button_initiate.configure("W.TButton", background="seashell4", foreground="red", font=("Helvetica", 12))
    app.initiate_button = ttk.Button(app.container, text="Initiate exchange", command=app.initiate_exchange, style="W.TButton")
    app.initiate_button.grid(row=1, column=2)

    # Create the solitary view
    solitary_ui = UISolitary(app.deck, app.container)
    solitary_ui.canvas.grid(row=3, column=1)

    root.mainloop()

if __name__ == "__main__":
    main()