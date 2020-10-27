from tkinter import *
from gui import GUI, run

win = Tk()
win.title("New Game")

players = []

C = Canvas(win, bg="blue", height=250, width=550)
filename = PhotoImage(file=r"resources\moleopoly background.png")
background_label = Label(win, image=filename)
background_label.place(x=0, y=0, relwidth=1, relheight=1)


def add_player():
    if e.get() != "" and len(players) < 4:
        players.append(e.get())
        listbox.insert(END, e.get())
        e.delete(0, END)


def start():
    if len(players) > 0:
        win.destroy()


title = Label(
    win, text="Mole - O - Poly", bg="#34b3ac", fg="white", font=("Comic Sans MS", 24)
)
b1 = Button(
    win,
    text="Add Player",
    bg="orange",
    fg="white",
    font="sans 12 bold",
    width=20,
    command=add_player,
)
e = Entry(win, text="Player Name", width=34)

t = Label(win, text="Players:", bg="#34b3ac", fg="white", font=("Comic Sans MS", 16))
listbox = Listbox(
    win,
    height=4,
    width=23,
    bg="white",
    activestyle="dotbox",
    font="sans 12 bold",
    fg="#34b3ac",
)

play = Button(
    win,
    text="Play!",
    bg="#2fba46",
    fg="white",
    font="sans 12 bold",
    width=10,
    command=start,
)

e.place(x=10, y=60)
e.insert(END, "Player Name")
b1.place(x=10, y=90)
title.place(x=0, y=0)
t.place(x=10, y=130)
listbox.place(x=10, y=165)
play.place(x=357, y=10)

C.pack()
win.mainloop()

if len(players) > 1:
    run(players)

