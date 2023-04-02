import json
import socket
import selectors
import threading
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.scrolledtext as scrolledtext
import tkinter.messagebox as messagebox
import tkinter.filedialog as filedialog
from PIL import ImageTk, Image

from cipher.Solitary import Solitary
from cipher.Deck import Deck
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
    show_deck = True
    can_build_deck = True

    cipher: Solitary = Solitary()

    window: tk.Tk
    build_deck_button: ttk.Button
    buttons_container: ttk.Frame
    shuffle_deck_button: ttk.Button
    send_deck_button: ttk.Button
    toggle_deck_button_container: ttk.Frame
    toggle_deck_button: ttk.Button
    send_message_button: ttk.Button

    window_icon: ImageTk.PhotoImage
    shuffle_deck_icon: ImageTk.PhotoImage
    send_icon: ImageTk.PhotoImage
    toggle_deck_icon: ImageTk.PhotoImage
    import_file_icon: ImageTk.PhotoImage

    messages_box: ttk.Frame
    encrypted_message_container: ttk.Frame
    encrypted_message_box: ttk.Label
    decrypted_message_container: ttk.Frame
    decrypted_message_box: ttk.Label

    ui_deck: UIDeck

    def __init__(self) :
        self.init_window()
        self.init_socket()
        self.init_icons()
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
        style.configure("Secondary.TLabel", background=MAIN_COLOR, foreground=SECONDARY_COLOR)
        style.configure("Red.TLabel", foreground="#ff0000", background=SECONDARY_COLOR)
        style.configure("Big.Secondary.TLabel", font=("Helvetica", 16))
        
        style.map("Main.TButton", background=[("active", MAIN_COLOR)], 
                                    foreground=[("active", SECONDARY_COLOR)], 
                                    relief=[("active", "sunken")])

        style.map("Secondary.TButton", background=[("active", SECONDARY_COLOR)],
                                         foreground=[("active", MAIN_COLOR)],
                                         relief=[("active", "sunken")])
        
        style.configure("TButton", borderwidth=0, font=("Helvetica", 12), cursor="hand2")
        style.configure("Main.TButton",  background=SECONDARY_COLOR, foreground=MAIN_COLOR)
        style.configure("Secondary.TButton",  background=MAIN_COLOR, foreground=SECONDARY_COLOR)
        style.configure("Big.Main.TButton",  font=("Helvetica", 16))
        style.configure("Big.Secondary.TButton",  font=("Helvetica", 16))
        style.configure("Small.Main.TButton",  font=("Helvetica", 10))
        style.configure("Small.Secondary.TButton",  font=("Helvetica", 10))

        style.configure("TFrame", background=SECONDARY_COLOR)
        style.configure("Secondary.TFrame", background=MAIN_COLOR)

    def init_icons(self):
        send_icon = Image.open("assets/images/send.png")
        send_icon = send_icon.resize((32, 32), Image.ANTIALIAS)
        self.send_deck_icon = ImageTk.PhotoImage(send_icon)

        shuffle_icon = Image.open("assets/images/shuffle.png")
        shuffle_icon = shuffle_icon.resize((32, 32), Image.ANTIALIAS)
        self.shuffle_deck_icon = ImageTk.PhotoImage(shuffle_icon)

        hide_icon = Image.open("assets/images/hide.png")
        hide_icon = hide_icon.resize((32, 32), Image.ANTIALIAS)
        self.hide_deck_icon = ImageTk.PhotoImage(hide_icon)

        import_icon = Image.open("assets/images/import.png")
        import_icon = import_icon.resize((32, 32), Image.ANTIALIAS)
        self.import_file_icon = ImageTk.PhotoImage(import_icon)

        show_icon = Image.open("assets/images/show.png")
        show_icon = show_icon.resize((32, 32), Image.ANTIALIAS)
        self.show_deck_icon = ImageTk.PhotoImage(show_icon)
        

    def init_home_page(self) :
        title = ttk.Label(self.window, 
                          text="CHIFFREMENT SOLITAIRE", 
                          padding=40,
                          width=750,
                          anchor="center",
                          style="Title.TLabel")
        title.pack(fill="x", side="top")
    
        if self.can_build_deck :
            self.build_deck_button = ttk.Button(self.window,
                                                text="Générer un jeu de cartes",
                                                command=self.init_deck_build_page,
                                                image=self.window_icon,
                                                compound="left",
                                                cursor="hand2",
                                                padding=10,
                                                style="Big.Main.TButton")
            self.build_deck_button.pack(expand=True)
        else :
            self.building_deck_label = ttk.Label(self.window, text="Votre communicant est en train de construire son jeu de cartes.\nMerci de patienter.", style="Red.TLabel", anchor="center")
            self.building_deck_label.pack(side="bottom", fill="both", expand=True)

    def init_deck_build_page(self) :
        self.build_deck_button.pack_forget()

        self.sock.send(json.dumps({"type": "building_deck"}).encode())

        self.ui_deck = UIDeck()
        self.ui_deck.canvas = ttk.Frame(self.window, padding=30)
        self.ui_deck.draw()
        self.ui_deck.canvas.pack(fill="both", expand=True)

        self.buttons_container = ttk.Frame(self.window, padding=30)
        self.buttons_container.pack(fill="both", side="bottom", anchor="center")

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

        self.send_deck_button = ttk.Button(self.buttons_container,
                                        text="Envoyer le jeu de cartes",
                                        command=self.send_deck,
                                        image=self.send_deck_icon,
                                        compound="left",
                                        cursor="hand2",
                                        padding=10,
                                        style="Small.Secondary.TButton")
        self.send_deck_button.pack(side="right", anchor="center")

    def init_messages_page(self) :

        if hasattr(self, "buttons_container"):
            self.buttons_container.pack_forget()

        self.ui_deck.draw_label.config(
            text="Jeu de cartes utilisé pour le chiffrement Solitaire.")
        self.ui_deck.draw_label.grid(row=0, column=0, columnspan=7, pady=15)

        self.toggle_deck_button_container = ttk.Frame(self.window, padding=10)
        self.toggle_deck_button_container.pack(side="top", fill="x", anchor="center", before=self.ui_deck.canvas)
        self.toggle_deck_button = ttk.Button(self.toggle_deck_button_container, 
                                             command=self.toggle_deck_frame,
                                             text="Masquer le jeu de cartes",
                                             image=self.hide_deck_icon, 
                                             compound="left",
                                             cursor="hand2",
                                             padding=10,
                                             style="Secondary.TButton")
        self.toggle_deck_button.pack(side="top", anchor="center")

        self.toggle_deck_frame()

        self.messages_box = ttk.Frame(self.window, padding=30)
        self.messages_box.pack(fill="both", expand=True)

        self.message_input_container = ttk.Frame(self.messages_box, padding=10)
        self.message_input_container.grid(row=0, column=0, sticky="nsew")

        self.message_input_label = ttk.Label(self.message_input_container, text="Message à envoyer :", style="Red.TLabel")
        self.message_input_label.grid(row=0, column=0, sticky="w", columnspan=3)
        self.message_input = ttk.Entry(self.message_input_container, width=70)
        self.message_input.grid(row=1, column=0, sticky="w", padx=(0, 10))
        self.message_input_button = ttk.Button(self.message_input_container, 
                                               command=self.send_message, 
                                               cursor="hand2",
                                               style="Small.Secondary.TButton",
                                               padding=10,
                                               image=self.send_deck_icon,
                                               compound="center")
        self.message_input_button.grid(row=1, column=1, sticky="w")

        self.import_message_button = ttk.Button(self.message_input_container,
                                                command=self.import_message,
                                                padding=10,
                                                cursor="hand2",
                                                style="Small.Secondary.TButton",
                                                image=self.import_file_icon,
                                                compound="center")
        self.import_message_button.grid(row=1, column=2, sticky="w", padx=10)

        self.messages_containers = ttk.Frame(self.messages_box, padding=10, style="Secondary.TFrame")
        self.messages_containers.grid(row=1, column=0, sticky="nsew")

        self.encrypted_message_container = ttk.Frame(self.messages_containers)
        self.encrypted_message_container.grid(row=0, column=0, padx=(0, 10))

        self.encrypted_message_box_label = ttk.Label(self.encrypted_message_container, text="Message chiffré :", style="Red.TLabel")
        self.encrypted_message_box_label.pack(side="top", anchor="w", fill="x")
        self.encrypted_message_box = scrolledtext.ScrolledText(self.encrypted_message_container, width=37, height=10)
        self.encrypted_message_box.pack(fill="both")

        self.decrypted_message_container = ttk.Frame(self.messages_containers)
        self.decrypted_message_container.grid(row=0, column=1, padx=(10, 0))

        self.decrypted_message_box_label = ttk.Label(self.decrypted_message_container, text="Message déchiffré :", style="Red.TLabel")
        self.decrypted_message_box_label.pack(side="top", anchor="w", fill="x")
        self.decrypted_message_box = scrolledtext.ScrolledText(self.decrypted_message_container, width=37, height=10)
        self.decrypted_message_box.pack(fill="both")


    def send_deck(self):
        messagebox.showinfo("Jeu de cartes", "Vous avez envoyé votre jeu de cartes à votre correspondant.")
        self.send_deck_button.pack_forget()
        self.shuffle_button.pack_forget()

        self.sock.send(json.dumps({"type": "deck", "deck": self.ui_deck.deck.serialize()}).encode())

        self.init_messages_page()

    def send_message(self) :
        message = self.message_input.get()
        if message == "" :
            return

        crypted = self.cipher.crypt(message, self.ui_deck.deck, is_encrypt=True)
        self.sock.send(json.dumps({"type": "message", "message": crypted}).encode())
        self.ui_deck.redraw()
        self.message_input.delete(0, "end")
        self.ui_deck.redraw()
        self.encrypted_message_box.config(state="normal")
        self.encrypted_message_box.insert("1.0", 'Envoyé -> ' + crypted + '\n', "send")
        self.encrypted_message_box.config(state="disabled")

        # remove special characters

        modified_message = message.upper()
        modified_message = modified_message.replace(" ", "")
        self.decrypted_message_box.config(state="normal")
        self.decrypted_message_box.insert("1.0", 'Envoyé -> ' + modified_message + '\n', "send")
        self.decrypted_message_box.config(state="disabled")

        self.encrypted_message_box.tag_config("send", foreground="green")
        self.decrypted_message_box.tag_config("send", foreground="green")


    def import_message(self) :
        file = filedialog.askopenfilename(initialdir = "../messages/",title = "Select file",filetypes = [("Text Files","*.txt")])
        if file == "" :
            return

        with open(file, "r") as f :
            self.message_input.insert(0, f.read())


    def on_message(self, connexion: socket.socket) :
        try:
            data = json.loads(connexion.recv(MAX_DATA_SIZE).decode())
        except json.decoder.JSONDecodeError:
            return

        if data["type"] == "ack" :
            self.can_build_deck = not data["is_someone_building_deck"]
        elif data["type"] == "building_deck" :
            self.on_building_deck_received()
        elif data["type"] == "deck" :
            self.on_deck_received(data["deck"])
        elif data["type"] == "message":
            self.encrypted_message_box.config(state="normal")
            self.encrypted_message_box.insert("1.0", 'Reçu -> ' + data["message"] + '\n', "received")
            self.encrypted_message_box.config(state="disabled")

            self.decrypted_message_box.config(state="normal")
            self.decrypted_message_box.insert("1.0", 'Reçu -> ' + self.cipher.crypt(data["message"], self.ui_deck.deck, is_encrypt=False) + '\n', "received")
            self.decrypted_message_box.config(state="disabled")

            self.encrypted_message_box.tag_config("received", foreground="red")
            self.decrypted_message_box.tag_config("received", foreground="red")

            self.ui_deck.redraw()

    def on_deck_received(self, deck: list) :
        messagebox.showinfo("Jeu de cartes", "Votre communicant vous a envoyé un jeu de cartes permettant de chiffrer le message.")
        self.can_build_deck = False
        if hasattr(self, "building_deck_label") :
            self.building_deck_label.pack_forget()
        else :
            self.build_deck_button.pack_forget()
        self.ui_deck = UIDeck(Deck.deserialize(deck).cards.copy())
        self.ui_deck.canvas = ttk.Frame(self.window, padding=30)
        self.ui_deck.draw()
        self.ui_deck.canvas.pack(fill="both", expand=True)
        self.ui_deck.canvas.pack(fill="both", expand=True)
        self.init_messages_page()

    def on_building_deck_received(self) :
        if hasattr(self, "build_deck_button") :
            self.build_deck_button.pack_forget()
        if hasattr(self, "window") :
            self.building_deck_label = ttk.Label(self.window, text="Votre communicant est en train de construire son jeu de cartes.\nMerci de patienter.", style="Red.TLabel", anchor="center")
            self.building_deck_label.pack(side="bottom", fill="both", expand=True)

    def toggle_deck_frame(self) :
        if self.show_deck :
            self.ui_deck.canvas.pack_forget()
            self.toggle_deck_button.config(image=self.show_deck_icon, text="Afficher le jeu de cartes")
            self.show_deck = False
        else :
            self.ui_deck.canvas.pack(fill="both", expand=True, after=self.toggle_deck_button_container)
            self.toggle_deck_button.config(image=self.hide_deck_icon, text="Masquer le jeu de cartes")
            self.show_deck = True

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