import json
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as font
import tkinter.scrolledtext as scrolledtext
import tkinter.messagebox as messagebox
import tkinter.filedialog as filedialog
from PIL import ImageTk, Image
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

MAIN_COLOR = "#364d53"
SECONDARY_COLOR = "#ffffff"
BACKGROUND_COLOR = "#f0f0f0"


class UISolitary:

    def __init__(self):

        self.close_app: bool = False
        self.cipher = Solitary()

        self.setup_socket()
        self.setup_window()

    def setup_socket(self):
        self.selector = selectors.DefaultSelector()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(ADDRESS)
        self.sock.setblocking(False)
        self.selector.register(self.sock, selectors.EVENT_READ, self.on_receive_message)
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def setup_window(self):
        self.window = tk.Tk()
        self.window.title("Chiffrement Solitaire")
        self.window.geometry("750x600")
        self.window.configure(background=SECONDARY_COLOR)
        image = Image.open("assets/images/icon.png")
        image = image.resize((40, 32), Image.ANTIALIAS)
        self.icon = ImageTk.PhotoImage(image)
        self.window.iconphoto(False, self.icon)

        self.main_container = ttk.Frame(self.window, style="Main.TFrame")
        self.main_container.pack(fill="both", expand=True)


        self.setup_styles()


        self.setup_entry_page()

        self.content_container = ttk.Frame(self.main_container, style="Main.TFrame")
        self.content_container.pack(side="top", fill="both", expand=True)

        self.create_deck_button = ttk.Button(self.content_container,
                            text="Créer un jeu de cartes",
                            command=self.on_build_deck,
                            cursor="hand2",
                            image=self.icon,
                            compound="left",
                            padding=10,
                            style="Secondary.TButton")
        self.create_deck_button.place(relx=0.5, rely=0.5, anchor="center")


    def setup_entry_page(self):
        self.title_container = ttk.Frame(self.main_container)
        self.title_container.pack(side="top", fill="x")

        title = ttk.Label(self.title_container, 
                          text="CHIFFREMENT SOLITAIRE",
                          style="TLabel", 
                          padding=20, 
                          width=750, 
                          anchor="center")
        title.pack(fill="both", expand=True)

    def setup_styles(self):

        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.style.map("Main.TButton", 
                       background=[("active", MAIN_COLOR)], 
                       foreground=[("active", SECONDARY_COLOR)], 
                       relief=[("active", "sunken")])
        self.style.map("Secondary.TButton", 
                       background=[("active", SECONDARY_COLOR)], 
                       foreground=[("active", MAIN_COLOR)],
                       relief=[("active", "sunken")])

        self.style.configure("Main.TFrame", background=BACKGROUND_COLOR)
        self.style.configure("Secondary.TFrame", background=MAIN_COLOR)
        self.style.configure("TLabel", font=("Bebas Neue", 24, "bold"), background=MAIN_COLOR, foreground=SECONDARY_COLOR)
        self.style.configure("TButton", borderwidth=0, font=("Bebas Neue",16,"normal"))
        self.style.configure("Main.TButton", background=SECONDARY_COLOR, foreground=MAIN_COLOR)
        self.style.configure("Small.Main.TButton", font=("Bebas Neue",10,"normal"))
        self.style.configure("Secondary.TButton", background=MAIN_COLOR, foreground=SECONDARY_COLOR)
        self.style.configure("Small.Secondary.TButton", font=("Bebas Neue",10,"normal"))
        self.style.configure("Mini.Secondary.TButton", font=("Bebas Neue", 8,"normal"))

    def on_build_deck(self):
        self.create_deck_button.place_forget()

        self.ui_deck = UIDeck()
        self.ui_deck.canvas = ttk.Frame(self.main_container, style="Main.TFrame")
        self.ui_deck.canvas.place(relx=0.5, rely=0.40, anchor="center")
        self.ui_deck.draw()

        image = Image.open("assets/images/shuffle.png")
        image = image.resize((32, 32), Image.ANTIALIAS)
        shuffle_icon = ImageTk.PhotoImage(image)
        self.shuffle_button = ttk.Button(self.main_container,
                                        text="Mélanger le jeu de cartes",
                                        command=self.
                                        ui_deck.shuffle,
                                        cursor="hand2",
                                        image=shuffle_icon,
                                        compound="left",
                                        padding=10,
                                        style="Small.Main.TButton")
        self.shuffle_button.place(relx=0.25, rely=0.9, anchor="center")

        self.validate_deck_button = ttk.Button(self.main_container,
                                               text="Valider le jeu de cartes",
                                               command=self.on_validate_deck,
                                               cursor="hand2",
                                               padding=10,
                                               style="Small.Secondary.TButton")
        self.validate_deck_button.place(relx=0.75, rely=0.9, anchor="center")

    def on_validate_deck(self):
        self.validate_deck_button.place_forget()
        self.sock.send(json.dumps({"type": "deck", "deck": self.ui_deck.deck.serialize()}).encode())
        self.draw_message_box()
        self.shuffle_button.place_forget()
        self.ui_deck.draw_label.config(
            text="Jeu de cartes utilisé pour le chiffrement Solitaire.")
        self.ui_deck.draw_label.grid(row=0, column=0, columnspan=7, pady=15)

        self.show_deck = True
        self.toggle_deck_button = ttk.Button(self.main_container, 
                                             text="Masquer le jeu de cartes", 
                                             command=self.toggleDeckFrame, 
                                             cursor="hand2",
                                             padding=10,
                                             style="Mini.Secondary.TButton")
        self.toggle_deck_button.place(relx=0.85, rely=0.19, anchor="center")

    def on_receive_deck(self, deck: bytes):
        messagebox.showinfo("Jeu de cartes", "Votre communicant vous a envoyé un jeu de cartes permettant de chiffrer le message.")
        self.create_deck_button.place_forget()
        self.ui_deck = UIDeck(Deck.deserialize(deck).cards.copy())
        self.ui_deck.canvas = ttk.Frame(self.main_container, style="Main.TFrame")
        self.ui_deck.canvas.place(relx=0.5, rely=0.40, anchor="center")
        self.ui_deck.draw()
        self.draw_message_box()
        self.ui_deck.draw_label.config(
            text="Jeu de cartes utilisé pour le chiffrement Solitaire.")
        self.ui_deck.draw_label.grid(row=0, column=0, columnspan=12, pady=10)

        self.show_deck = True
        self.toggle_deck_button = ttk.Button(self.main_container, 
                                             text="Masquer le jeu de cartes", 
                                             command=self.toggleDeckFrame,
                                             cursor="hand2",
                                             style="Small.Secondary.TButton")
        self.toggle_deck_button.place(relx=0.75, rely=0.5, anchor="center")

    def on_receive_message(self, conn: socket.socket, mask: selectors.EVENT_READ):
        try:
            data = json.loads(conn.recv(MAX_DATA_SIZE).decode())
        except json.decoder.JSONDecodeError:
            return
        if data["type"] == "deck":
            self.on_receive_deck(data["deck"])
        elif data["type"] == "message":
            message = self.cipher.crypt(data["message"], self.ui_deck.deck, is_encrypt=False)
            self.received_messages_box.config(state="normal")
            self.received_messages_box.insert("1.0", message + '\n')
            self.received_messages_box.config(state="disabled")
            self.ui_deck.redraw()

    def on_send_message(self, message: str = None):
        if message is None or len(message) == 0:
            message = self.message_input.get()
        message = self.cipher.crypt(message, self.ui_deck.deck, is_encrypt=True)
        self.sock.send(json.dumps({"type": "message", "message": message}).encode())
        self.message_input.delete(0, tk.END)
        self.ui_deck.redraw()

    def draw_message_box(self):
        self.messages_container = ttk.Frame(self.main_container, style="Secondary.TFrame", padding=10)
        self.messages_container.place(relx=0.5, rely=0.85, anchor="center")

        image_send = Image.open("assets/images/send.png")
        image_send = image_send.resize((40, 40), Image.ANTIALIAS)
        self.icon_send = ImageTk.PhotoImage(image_send)
        self.send_message_button = ttk.Button(self.messages_container, 
                                            #   text="Envoyer le message", 
                                              image=self.icon_send,
                                              compound="center",
                                              command=self.on_send_message,
                                              cursor="hand2",
                                              style="Secondary.TButton"
                                              )
        
        image_import = Image.open("assets/images/import.png")
        image_import = image_import.resize((40, 40), Image.ANTIALIAS)
        self.icon_import = ImageTk.PhotoImage(image_import)
        self.import_file_button = ttk.Button(self.messages_container,
                                                # text="Importer un fichier",
                                                image=self.icon_import,
                                                compound="center",
                                                command=self.import_file,
                                                cursor="hand2",
                                                style="Secondary.TButton")
        self.import_file_button.grid(row=0, column=1)
        self.send_message_button.grid(row=0, column=1)

        self.message_input = ttk.Entry(self.messages_container, width=70)
        self.message_input.grid(row=0, column=0)

        self.received_messages_box = scrolledtext.ScrolledText(self.messages_container, width=80, height=5)
        self.received_messages_box.grid(row=1, column=0, padx=10, pady=10, columnspan=2)

    def toggleDeckFrame(self):
        if self.show_deck:
            self.ui_deck.canvas.place_forget()
            self.toggle_deck_button.config(text="Afficher le jeu de cartes")
            self.show_deck = False
            self.messages_container.place(relx=0.5, rely=0.5, anchor="center")
        else:
            self.ui_deck.canvas.place(relx=0.5, rely=0.40, anchor="center")
            self.toggle_deck_button.config(text="Masquer le jeu de cartes")
            self.show_deck = True
            self.messages_container.place(relx=0.5, rely=0.85, anchor="center")

    def import_file(self):
        filename = filedialog.askopenfilename(initialdir = "../messages/",title = "Select file",filetypes = [("Text Files","*.txt")])
        if filename == "":
            return
        with open(filename, "r") as f:
            self.on_send_message(f.read())

    def on_closing(self):
        self.thread.join()
        self.selector.unregister(self.sock)
        self.sock.close()
        self.selector.close()

    def run(self):
        while not self.close_app:
            events = self.selector.select(timeout=0)
            for key, mask in events:
                callback = key.data
                callback(key.fileobj, mask)
