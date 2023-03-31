import json
import socket
import selectors
import threading
import tkinter as tk
import tkinter.ttk as ttk
from PIL import ImageTk, Image

from cipher.Solitary import Solitary
from ui.UIDeck import UIDeck

HOST = socket.gethostbyname(socket.gethostname())
PORT = 65432
ADDRESS = (HOST, PORT)
MAX_DATA_SIZE = 4000

MAIN_COLOR = "#364d53"
SECONDARY_COLOR = "#ffffff"
BACKGROUND_COLOR = "#f0f0f0"

class UISolitary : 

    selector: selectors.DefaultSelector 
    sock: socket.socket

    close_app = False
    can_build_deck = True

    cipher: Solitary = Solitary()

    window: tk.Tk
    build_deck_button: ttk.Button
    buttons_container: ttk.Frame
    shuffle_deck_button: ttk.Button
    send_deck_button: ttk.Button

    window_icon: ImageTk.PhotoImage
    shuffle_deck_icon: ImageTk.PhotoImage
    send_icon: ImageTk.PhotoImage

    messages_box: ttk.Frame
    encrypted_message_container: ttk.Frame
    encrypted_message_box: ttk.Label
    decrypted_message_container: ttk.Frame
    decrypted_message_box: ttk.Label

    ui_deck: UIDeck

    def __init__(self) :
        self.init_socket()
        self.init_window()
        self.init_styles()
        self.init_home_page()

    def init_socket(self) :
        self.selector = selectors.DefaultSelector()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(ADDRESS)
        self.sock.setblocking(False)
        self.selector.register(self.sock, selectors.EVENT_READ, self.on_message)
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def init_window(self) :
        self.window = tk.Tk()
        self.window.title("Chiffrement Solitaire")
        self.window.geometry("750x600")
        self.window.configure(background=BACKGROUND_COLOR)
        self.window.resizable(False, False)

        image = Image.open("assets/images/icon.png")
        image = image.resize((40, 32), Image.ANTIALIAS)
        self.window_icon = ImageTk.PhotoImage(image)
        self.window.iconphoto(False, self.window_icon)

    def init_styles(self) :
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("*", font=("Helvetica", 12))
        style.configure("TLabel", font=("Helvetica", 12), backgroun=SECONDARY_COLOR)
        style.configure("Title.TLabel", 
                        font=("Helvetica", 26, "bold"), 
                        background=MAIN_COLOR, 
                        foreground=SECONDARY_COLOR)
        
        style.map("Main.TButton", background=[("active", MAIN_COLOR)], 
                                    foreground=[("active", SECONDARY_COLOR)], 
                                    relief=[("active", "sunken")])

        style.map("Secondary.TButton", background=[("active", SECONDARY_COLOR)],
                                         foreground=[("active", MAIN_COLOR)],
                                         relief=[("active", "sunken")])
        
        style.configure("TButton", borderwidth=0)
        style.configure("Main.TButton",  background=SECONDARY_COLOR, foreground=MAIN_COLOR)
        style.configure("Secondary.TButton",  background=MAIN_COLOR, foreground=SECONDARY_COLOR)
        style.configure("Big.Main.TButton",  font=("Helvetica", 16))
        style.configure("Big.Secondary.TButton",  font=("Helvetica", 16))
        style.configure("Small.Main.TButton",  font=("Helvetica", 10))
        style.configure("Small.Secondary.TButton",  font=("Helvetica", 10))

        style.configure("TFrame", background=SECONDARY_COLOR)
        style.configure("Secondary.TFrame", background=MAIN_COLOR)
        

    def init_home_page(self) :
        title = ttk.Label(self.window, 
                          text="CHIFFREMENT SOLITAIRE", 
                          padding=40,
                          width=750,
                          anchor="center",
                          style="Title.TLabel"
                          )
        title.pack(fill="x", side="top")
    
        self.build_deck_button = ttk.Button(self.window,
                                            text="Générer un jeu de cartes",
                                            command=self.init_deck_build_page,
                                            image=self.window_icon,
                                            compound="left",
                                            cursor="hand2",
                                            padding=10,
                                            style="Big.Main.TButton")
        self.build_deck_button.pack(expand=True)

    def init_messages_page(self) :
        self.messages_box = ttk.Frame(self.window, padding=10)
        self.messages_box.pack(fill="both", expand=True)

        self.encrypted_message_container = ttk.Frame(self.messages_box, padding=10)
        self.encrypted_message_container.pack(fill="x", expand=True)

        self.decrypted_message_container = ttk.Frame(self.messages_box, padding=10)
        self.decrypted_message_container.pack(fill="x", expand=True)

        # self.decrypted_message_box = ttk.Frame(self.messages_box, padding=10)
        # self.decrypted_message_box.pack(fill="x", expand=True)


    def init_deck_build_page(self) :
        self.build_deck_button.pack_forget()

        self.ui_deck = UIDeck()
        self.ui_deck.canvas = ttk.Frame(self.window, padding=30)
        self.ui_deck.draw()
        self.ui_deck.canvas.pack(fill="both", expand=True)

        self.buttons_container = ttk.Frame(self.window, padding=30)
        self.buttons_container.pack(fill="both", side="bottom", anchor="center")

        shuffle_icon = Image.open("assets/images/shuffle.png")
        shuffle_icon = shuffle_icon.resize((32, 32), Image.ANTIALIAS)
        self.shuffle_deck_icon = ImageTk.PhotoImage(shuffle_icon)

        self.shuffle_button = ttk.Button(self.buttons_container,
                                        text="Mélanger le jeu de cartes",
                                        command=self.
                                        ui_deck.shuffle,
                                        cursor="hand2",
                                        image=self.shuffle_deck_icon,
                                        compound="left",
                                        padding=10,
                                        style="Small.Main.TButton")
        self.shuffle_button.pack(side="left", anchor="center")

        send_icon = Image.open("assets/images/send.png")
        send_icon = send_icon.resize((32, 32), Image.ANTIALIAS)
        self.send_deck_icon = ImageTk.PhotoImage(send_icon)
        self.validate_deck_button = ttk.Button(self.buttons_container,
                                        text="Envoyer le jeu de cartes",
                                        command=self.send_deck,
                                        cursor="hand2",
                                        image=self.send_deck_icon,
                                        compound="left",
                                        padding=10,
                                        style="Small.Secondary.TButton")
        self.validate_deck_button.pack(side="right", anchor="center")

    def send_deck(self):
        self.send_deck_button.pack_forget()
        self.shuffle_button.pack_forget()

        self.sock.send(json.dumps({"type": "deck", "deck": self.ui_deck.deck}).encode())

    def on_message(self, connexion: socket.socket) :
        try:
            data = json.loads(connexion.recv(MAX_DATA_SIZE).decode())
        except json.decoder.JSONDecodeError:
            return
        
        if data["type"] == "deck" :
            self.on_deck_received(data["deck"])

    def on_deck_received(self, deck: list) :
        self.can_build_deck = False
        self.build_deck_button.pack_forget()
        self.ui_deck = UIDeck(self.window, deck)
        self.ui_deck.canvas.pack(fill="both", expand=True)

    def on_close(self) :
        self.thread.join()
        self.selector.unregister(self.sock)
        self.sock.close()
        self.selector.close()

    def run(self) :
        while not self.close_app:
            events = self.selector.select(timeout=0)
            for key, mask in events:
                callback = key.data
                callback(key.fileobj)