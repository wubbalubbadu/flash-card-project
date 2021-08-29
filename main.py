from tkinter import *
import pandas
import random
from tkinter import messagebox
import os

BACKGROUND_COLOR = "#B1DDC6"
SMALL_FONT = ("Ariel", 40, "italic")
BIG_FONT = ("Ariel", 60, "bold")
FRONT_FILL = "Black"
BACK_FILL = "white"
FRONT_LANG = "English"
BACK_LANG = "Chinese"
START_INDEX = 0
END_INDEX = 4500

REVIEW_FILE_PATH = "data/words_to_review.csv"
LEARNING_FILE_PATH = "data/words_to_learn.csv"
LIBRARY_FILE_PATH = "data/en5000.csv"


def get_data():
    global data_list, data
    # reviewing mode:
    if radiostate.get() == 1:
        try:
            if os.path.getsize(REVIEW_FILE_PATH) < 2:
                messagebox.showinfo(message="review mode done!")
                radiostate.set(0)
                data = get_library()
            else:
                data = pandas.read_csv(REVIEW_FILE_PATH)
        except FileNotFoundError:
            radiostate.set(0)
            messagebox.showinfo(message="No word in word bank")
            data = get_library()
    # learning mode:
    else:
        try:
            if os.path.getsize(LEARNING_FILE_PATH) < 2:
                data = get_library()
            else:
                data = pandas.read_csv(LEARNING_FILE_PATH)
        except FileNotFoundError:
            data = get_library()
    data_list = data.to_dict(orient="records")


def get_library():
    return pandas.read_csv(LIBRARY_FILE_PATH, names=[FRONT_LANG, BACK_LANG],
                           skiprows=START_INDEX, nrows=END_INDEX - START_INDEX)


def generate():
    global curr_word, flip_timer
    root.after_cancel(flip_timer)
    curr_word = random.choice(data_list)
    flash_card.itemconfig(card, image=front_img)
    flash_card.itemconfig(word, text=curr_word[FRONT_LANG], font=BIG_FONT, fill=FRONT_FILL)
    flash_card.itemconfig(header, text=FRONT_LANG, fill=FRONT_FILL)
    flip_timer = root.after(3000, flip)


def unknown_word():
    review_list = []
    try:
        if os.path.getsize(REVIEW_FILE_PATH) < 2:
            pass
        else:
            review_df = pandas.read_csv(REVIEW_FILE_PATH)
            review_list = review_df.to_dict(orient="records")
    except FileNotFoundError:
        pass
    finally:
        review_list.append(curr_word)
        new_review_list = pandas.DataFrame(review_list)
        print(new_review_list)
        new_review_list.to_csv(REVIEW_FILE_PATH, index=False)
        generate()


def known_word():
    global data_list
    if curr_word in data_list:
        data_list.remove(curr_word)
    new_data_list = pandas.DataFrame(data_list)
    new_data_list.to_csv(LEARNING_FILE_PATH, index=False)
    if radiostate.get() == 1:
        new_data_list.to_csv(REVIEW_FILE_PATH, index=False)
    if len(data_list) == 0:
        get_data()
    generate()


def flip():
    flash_card.itemconfig(card, image=back_img)
    flash_card.itemconfig(word, text=curr_word[BACK_LANG], fill=BACK_FILL)
    flash_card.itemconfig(header, text=BACK_LANG, fill=BACK_FILL)


# UI
root = Tk()
root.title("English 5000")
root.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
flip_timer = root.after(3000, flip)

# radiostate
frame = Frame()
radiostate = IntVar()
review_button = Radiobutton(frame, text="Review Mode", value=1, variable=radiostate,
                            command=get_data, bg=BACKGROUND_COLOR, width=13)
learn_button = Radiobutton(frame, text="Learning Mode", value=0, variable=radiostate,
                           command=get_data, bg=BACKGROUND_COLOR, width=13)
review_button.pack()
learn_button.pack()
frame.grid(row=1, column=2)
radiostate.set(0)

data_list = []
data = None
get_data()
curr_word = random.choice(data_list)
print(curr_word)

# flashcard
front_img = PhotoImage(file="images/card_front.png")
back_img = PhotoImage(file="images/card_back.png")
flash_card = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card = flash_card.create_image(400, 263, image=front_img)
header = flash_card.create_text(400, 150, text=FRONT_LANG, font=SMALL_FONT)
word = flash_card.create_text(400, 263, text=curr_word[FRONT_LANG], font=BIG_FONT, fill=FRONT_FILL)
flash_card.grid(row=0, column=0, columnspan=2)

# buttons
incorrect_icon = PhotoImage(file="images/wrong.png")
incorrect_button = Button(image=incorrect_icon, highlightthickness=0, bd=0, command=unknown_word)
incorrect_button.grid(row=1, column=0)
correct_icon = PhotoImage(file="images/right.png")
correct_button = Button(image=correct_icon, highlightthickness=0, bd=0, command=known_word)
correct_button.grid(row=1, column=1)

root.mainloop()
