import socket
from typing import Optional
from tkinter import Label, Misc, Canvas, Toplevel, filedialog, ttk
from .UIDeck import UIDeck
from cipher.Deck import Deck

from cipher.Solitary import Solitary

class UISolitary:
    def __init__(self, ui_deck: UIDeck, parent: Optional[Misc] = None):
        self.solitary = Solitary()
        self.ui_deck = ui_deck

        # Create the text box to enter the message
        self.canvas = Canvas(parent, width=100, height=600)

        self.message_input = ttk.Entry(self.canvas, width=10)
        self.message_input.grid(row=1, column=1)

        # Create the button to encrypt the message and send it
        style_button = ttk.Style()
        style_button.configure("W.TButton", background="seashell4", foreground="red", font=("Helvetica", 12))
        self.encrypt_button = ttk.Button(self.canvas, text="Encrypt", command=self.encrypt, style="W.TButton")
        self.encrypt_button.grid(row=1, column=2)

        #self.text_from_file()

    def encrypt(self):
        message = self.message_input.get()
        crypted_message = self.solitary.crypt(message, self.ui_deck.deck, True)

    def decrypt(self):
        message = self.message_input.get()
        decrypted_message = self.solitary.crypt(message, self.ui_deck.deck, False)

    def text_from_file(self):
        filename = filedialog.askopenfilename()
        with open(filename, "r") as file:
            #only allow text files
            if filename.endswith(".txt"):
                self.message_input.delete(0, "end")
                self.message_input.insert("1", file.read())
            else:
                # show error message if file is not a text file in a new window
                error_window = Toplevel()
                error_window.title("Error")
                error_window.geometry("300x100")
                error_window.resizable(False, False)
                error_window.configure(background="white")
                error_label = Label(error_window, text="Please select a text file", bg="white", fg="red")
                error_label.pack(anchor="center", expand=True)