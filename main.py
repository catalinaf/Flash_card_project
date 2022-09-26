from tkinter import *
import pandas as pd
import random

BACKGROUND_COLOR = "#B1DDC6"
current_word = {}
words_list = {}

try:
    words = pd.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_words = pd.read_csv("data/french_words.csv")
    words_list = original_words.to_dict(orient="records")
else:
    words_list = words.to_dict(orient="records")


# ---------------------------- SORT WORDS ------------------------------- #
def knows_word():
    global words_list
    if len(words_list) > 1:
        words_list.remove(current_word)
        generate_word()
        df = pd.DataFrame(words_list)
        df.to_csv("data/words_to_learn.csv", index=False)
    else:
        canvas.itemconfig(title, text="", fill="black")
        canvas.itemconfig(word, text="That's it. Good job!", fill="black")
        window.after_cancel(flip_timer)


# ---------------------------- GENERATE WORD ------------------------------- #
def generate_word():
    global current_word, flip_timer
    window.after_cancel(flip_timer)

    current_word = random.choice(words_list)

    canvas.itemconfig(title, text="French", fill="black")
    canvas.itemconfig(word, text=current_word["French"], fill="black")
    canvas.itemconfig(canvas_image, image=front_image)

    flip_timer = window.after(3000, func=flip_card)


# ---------------------------- FLIP CARD ------------------------------- #
def flip_card():
    canvas.itemconfig(title, text="English", fill="white")
    canvas.itemconfig(word, text=current_word["English"], fill="white")
    canvas.itemconfig(canvas_image, image=back_image)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)

back_image = PhotoImage(file="images/card_back.png")
front_image = PhotoImage(file="images/card_front.png")

canvas_image = canvas.create_image(400, 263, image=front_image)
title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))
canvas.grid(column=0, row=0, columnspan=2)

wrong_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_image, command=generate_word, highlightthickness=0)
wrong_button.grid(column=0, row=1)

right_image = PhotoImage(file="images/right.png")
right_button = Button(image=right_image, command=knows_word, highlightthickness=0)
right_button.grid(column=1, row=1)

generate_word()
window.mainloop()
