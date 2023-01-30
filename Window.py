import tkinter as tk

def onEnter(e, button):
    button["background"] = "red"
    button["foreground"] = "white"

def onLeave(e, button):
    button["background"] = "red"
    button["foreground"] = "black"
    

class Window:
    def __init__(self, master=None):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.frame.pack()

        self.button = tk.Button(self.frame, text="QUIT", fg="red", command=self.frame.quit)
        self.button.pack(side=tk.LEFT)
        self.button.bind("<Enter>", lambda e: onEnter(e, self.button))
        self.button.bind("<Leave>", lambda e: onLeave(e, self.button))

        self.hi_there = tk.Button(self.frame, text="Hello", command=self.say_hi)
        self.hi_there.pack(side=tk.LEFT)

    def say_hi(self):
        print("hi there, everyone!")


root = tk.Tk()
root.resizable(True, True)

label = tk.Label(root, text="Hello World")

app = Window(root)
root.mainloop()