import random
from tkinter import *
import pandas

BACKGROUND_COLOR = "#B1DDC6"
FONT_ITALIC = ("Arial", 40, "italic")
FONT_BOLD = ("Arial", 60, "bold")
FONT_BTN = ("Arial", 30, "bold")
current_word = {}

# -------------------- Load data -------------------- #
try:
    data = pandas.read_csv("./data/words_to_learn.csv").to_dict(orient="records")
except:
    data = pandas.read_csv("./data/french_words.csv").to_dict(orient="records")
else:
    if len(data) <= 0:
        data = pandas.read_csv("./data/french_words.csv").to_dict(orient="records")

# -------------------- Card Operations -------------------- #
def random_card():
    global current_word
    if len(data) > 0:
        random_word = random.choice(data)
        current_word = random_word

        current_title = flash_card.itemcget(card_title, "text")
        if current_title =="English":
            flip_card()

        # Set card info
        flash_card.itemconfig(card_title, text="French")
        flash_card.itemconfig(card_word, text = random_word["French"])
    else:
        flash_card.itemconfig(card_title, text="Well done!")
        flash_card.itemconfig(card_word, text="No words left to learn!\nRestart the app to start over.", font =("Arial", 24))


def flip_card():
    global current_word
    current_title = flash_card.itemcget(card_title, "text")

    if current_title == "French":
        flash_card.itemconfig(card_image, image = img_card_back)
        flash_card.itemconfig(card_title, fill = "white", text = "English")
        flash_card.itemconfig(card_word, fill="white", text = current_word["English"])
    else:
        flash_card.itemconfig(card_image, image=img_card_front)
        flash_card.itemconfig(card_title, fill="black", text = "French")
        flash_card.itemconfig(card_word, fill="black", text = current_word["French"])

def green_btn_press():
    global data
    global current_word

    data.remove(current_word)
    pandas.DataFrame(data).to_csv("./data/words_to_learn.csv", index=False)
    random_card()


# -------------------- UI SETUP -------------------- #
window = Tk()
window.title("Flash cards")
window.config(bg=BACKGROUND_COLOR,
              pady= 50,padx= 50)

# ----- Card ----- #
flash_card = Canvas(bg = BACKGROUND_COLOR, width=800, height=526, highlightthickness=0)
img_card_front = PhotoImage(file="./images/card_front.png")
img_card_back = PhotoImage(file="./images/card_back.png")

card_image = flash_card.create_image(400, 263, image = img_card_front)

card_title = flash_card.create_text(400, 150, text="Title", font=FONT_ITALIC)
card_word = flash_card.create_text(400, 263, text="word", font=FONT_BOLD)

flash_card.grid(rowspan=2, columnspan=3, row=0, column=0)

# ----- Buttons ----- #
img_wrong = PhotoImage(file="./images/wrong.png")
btn_wrong = Button(image=img_wrong, highlightthickness=0, command= random_card)
btn_wrong.grid(row=2, column=0)

img_correct = PhotoImage(file="./images/right.png")
btn_correct = Button(image=img_correct, highlightthickness=0, command= green_btn_press)
btn_correct.grid(row=2, column=2)

btn_flip = Button(text= "Flip", font=FONT_BTN, command= flip_card)
btn_flip.grid(row=2, column=1)


random_card()

window.mainloop()