import tkinter as tk
import tkinter.ttk as ttk

class Decrypt:

    # def __init__(self):
    #     # get the deck from the encrypter

    def run(self):
        # Create the main window
        root = tk.Tk()
        root.title("Run Decrypt")
        root.geometry("500x500")

        # Create the main frame
        container = ttk.Frame(root, padding=30)
        container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Create the title
        title = ttk.Label(container, text="Run Decrypt", font=("Helvetica", 36), padding=30).grid(row=1, column=1)

        # Create the deck view
        # receive the deck from the encrypter

        # Create the solitary view

        root.mainloop()
