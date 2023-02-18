import json
from multiprocessing import Process, current_process
import socket
from typing import Optional
import tkinter as tk
from .UIDeck import UIDeck
from cipher.Deck import Deck
import tkinter.ttk as ttk

from cipher.Solitary import Solitary

class UISolitary:

    root : tk.Tk
    container : tk.Frame


    def __init__(self):
        with open("conf.json", "r") as f:
            conf = json.load(f)
            self.host = conf["host"]
            self.port = conf["port"]
            self.data_size = conf["data_size"]


        # self.solitary = Solitary()
        # self.ui_deck = ui_deck

        # # Create the text box to enter the message
        # self.canvas = Canvas(parent, width=100, height=600)

        # self.message_input = ttk.Entry(self.canvas, width=10)
        # self.message_input.grid(row=1, column=1)

        # # Create the button to encrypt the message and send it
        # style_button = ttk.Style()
        # style_button.configure("W.TButton", background="seashell4", foreground="red", font=("Helvetica", 12))
        # self.encrypt_button = ttk.Button(self.canvas, text="Encrypt", command=self.encrypt, style="W.TButton")
        # self.encrypt_button.grid(row=1, column=2)

    def run_ui(self, args):
        #self.process_ui = current_process()
        print(args)
        self.init_window()
        self.root.mainloop()

    def init_window(self):
        # Create the main window
        self.root = tk.Tk()
        self.root.title("Run Encrypt")
        self.root.geometry("900x550")

        # Create the main frame
        self.container = ttk.Frame(self.root, padding=30)
        self.container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Create the title
        title = ttk.Label(self.container, text="Run Encrypt", font=("Helvetica", 36, "bold"), padding=30).grid(row=1, column=1)

        # Button to initiate the exchange
        initiate_button = ttk.Button(self.container, text="Initiate exchange", command=lambda: self.on_initiate(initiate_button))
        initiate_button.grid(row=1, column=2)

    def on_initiate(self, button: ttk.Button):
        self.process_ui.terminate()

        # Create the deck view
        self.deck_ui = UIDeck()
        self.deck_ui.canvas = tk.Canvas(self.container, width=100, height=600)
        self.deck_ui.canvas.grid(row=2, column=1, pady=30)

        self.deck_ui.draw()

        # Disable the initiate button
        button.destroy()
        
        # Create the button to validate the exchange
        validate_button = ttk.Button(self.container, text="validate", command=lambda: self.on_validate_deck(validate_button))
        validate_button.grid(row=5, column=15, columnspan=2)

    def on_validate_deck(self, button: ttk.Button):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((self.host, self.port))
            # send the deck to the other app
            sock.sendall(json.dumps(self.deck_ui.deck.serialize()).encode())
            sock.close()

        # Disable the validate button
        button.destroy()

    def on_wait_for_deck(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind((self.host, self.port))
            sock.listen()
            conn, addr = sock.accept()
            with conn:
                print("Connected by", addr)
                data = conn.recv(self.data_size)
                if data:
                    print(data.decode())

                    # deserialize the deck
                    #self.deck = Deck.deserialize(json.loads(data.decode()))
                    # draw the deck
                    # self.deck_ui.draw()
                    # close the socket
                    sock.close()



    # def encrypt(self):
    #     message = self.message_input.get()
    #     crypted_message = self.solitary.crypt(message, self.ui_deck.deck, True)

    # def decrypt(self):
    #     message = self.message_input.get()
    #     decrypted_message = self.solitary.crypt(message, self.ui_deck.deck, False)

    # def text_from_file(self):
    #     filename = filedialog.askopenfilename()
    #     with open(filename, "r") as file:
    #         #only allow text files
    #         if filename.endswith(".txt"):
    #             self.message_input.delete(0, "end")
    #             self.message_input.insert("1", file.read())
    #         else:
    #             # show error message if file is not a text file in a new window
    #             error_window = Toplevel()
    #             error_window.title("Error")
    #             error_window.geometry("300x100")
    #             error_window.resizable(False, False)
    #             error_window.configure(background="white")
    #             error_label = Label(error_window, text="Please select a text file", bg="white", fg="red")
    #             error_label.pack(anchor="center", expand=True)
