from typing import Optional
from tkinter import Misc, Canvas, PhotoImage
from PIL import Image, ImageTk
from cipher.Card import Card, CardSuit, CardValue

IMAGE_SIZE = (55, 72)

class UICard:

    def __init__(self, card: Card, parent: Optional[Misc] = None):
        self.card = card

        # Create the canvas
        self.canvas = Canvas(parent, width=IMAGE_SIZE[0] + 1, height=IMAGE_SIZE[1] + 1)

        # Create the image
        links = self.get_card_links()
        self.image_normal = Image.open(fp=links[0])
        self.image_normal = self.resize_image(self.image_normal)

        # Create the hover image
        self.image_hover = Image.open(fp=links[1])
        self.image_hover = self.resize_image(self.image_hover)

        # Create the tk images
        self.tk_image_normal = ImageTk.PhotoImage(self.image_normal)
        self.tk_image_hover = ImageTk.PhotoImage(self.image_hover)

        # Create the object image and bind the events
        self.object_image = self.canvas.create_image(2, 2, image=self.tk_image_normal, anchor="nw")
        self.canvas.bind("<Enter>", self.on_enter)
        self.canvas.bind("<Leave>", self.on_leave)

    # Get the card links to the images
    def get_card_links(self):
        folder = "./assets/images/" + str(self.card.suit).lower()
        return [
            folder + "/" + self.card.suit  + "-" + str(self.card.rank) + ".png",
            folder + "/" + self.card.suit  + "-" + str(self.card.rank) + "-hover.png"
        ]

    # Resize the image to the size of the card
    def resize_image(self, image: Image):
        return image.resize(IMAGE_SIZE, Image.ANTIALIAS)

    def on_enter(self, event):
        self.canvas.itemconfig(self.object_image, image=self.tk_image_hover)
        self.canvas.tag_bind(self.object_image, '<Leave>', self.on_leave)

    def on_leave(self, event):
        self.canvas.itemconfig(self.object_image, image=self.tk_image_normal)
        self.canvas.tag_bind(self.object_image, '<Enter>', self.on_enter)
