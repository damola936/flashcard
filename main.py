import random
from tkinter import *
from tkinter import messagebox
import pandas as pd

BACKGROUND_COLOR = "#B1DDC6"
FONT_NAME = "SF Pro Display"
timer = None
COUNT = 5

dataset = pd.read_csv("data/french_words.csv")
french = list(dataset["French"])
english = list(dataset["English"])
rand_index = random.randint(1, len(french))


# -------------------------------------- FUNCTIONALITY ------------------------------------- #

def change():
    item_word = canvas.itemcget(word, "text")
    print(item_word)
    for index, char in enumerate(english):
        if char == item_word:
            return index


def count_down(count=COUNT):
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1)
    elif count == 0:
        french_index = change()
        window.after_cancel(timer)
        print("I have hit")
        canvas.itemconfig(image, image=flash_card_back)
        canvas.itemconfig(language, text="French", font=(FONT_NAME, 30, "italic"))
        canvas.itemconfig(word, text=french[french_index], font=(FONT_NAME, 40, "bold"))


def got_correct(event):
    item_word = canvas.itemcget(word, "text")
    for index, char in enumerate(english):
        if char == item_word:
            french.pop(index)
            english.pop(index)
            got_wrong(event)


def got_wrong(event):
    english_text = random.choice(english)
    canvas.itemconfig(image, image=flash_card_front)
    canvas.itemconfig(language, text="English", font=(FONT_NAME, 30, "italic"))
    canvas.itemconfig(word, text=english_text, font=(FONT_NAME, 40, "bold"))
    count_down()


# -------------------------------------- UI ------------------------------------------------ #
window = Tk()
window.title("Flash Card App")
window.config(padx=20, pady=20)
window.config(bg=BACKGROUND_COLOR)

canvas = Canvas(width=820, height=630, highlightthickness=0)
flash_card_front = PhotoImage(file="images/card_front.png")
flash_card_back = PhotoImage(file="images/card_back.png")
right = PhotoImage(file="images/right.png")
wrong = PhotoImage(file="images/wrong.png")
image = canvas.create_image(410, 263, image=flash_card_front, tag="image-front")
language = canvas.create_text(410, 100, text="English", font=(FONT_NAME, 30, "italic"), tags="e-language")
word = canvas.create_text(410, 200, text=english[rand_index], font=(FONT_NAME, 40, "bold"), tags="e-word")
canvas.create_image(210, 580, image=wrong, tag="wrong")
canvas.create_image(610, 580, image=right, tag="right")
canvas.pack()
canvas.config(bg=BACKGROUND_COLOR)
canvas.tag_bind("right", "<Button-1>", got_correct)
canvas.tag_bind("wrong", "<Button-1>", got_wrong)
count_down()

window.mainloop()
