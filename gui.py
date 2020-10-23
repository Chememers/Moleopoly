from tkinter import Tk, Canvas
from tkinter.constants import BOTH
from moleopoly import Board, ElementSquare
from const import CENTERSIZE, SIZE, SQSHORT, SQLONG


class ElementSquareGUI:
    def __init__(self, canvas, square, side):
        self.canvas = canvas
        self.square = square
        self.side = side


class GUI(Board):
    def __init__(self, master, players: list):
        super().__init__(*players)
        self.win = master
        self.setup_board()

    def setup_board(self):
        self.canvas = Canvas(self.win, bg="white", width=SIZE, height=SIZE)
        self.canvas.pack(fill=BOTH)
        self.canvas.create_rectangle(
            SQLONG, SQLONG, SQLONG + CENTERSIZE, SQLONG + CENTERSIZE, fill="#74BBFB"
        )

        # dirs = ("W", "N", "E", "S")
        # ranges = ((1, 8), (9, 16), (17, 24), (25, 32))
        # for i in range(4):
        #     for j in range(*ranges[i]):
        #         sq = self.squares[j]
        #         if isinstance(sq, ElementSquare):
        #             ElementSquareGUI(self.canvas, sq, dirs[i])


players = ("Aditya", "Gowtham", "Hari")
# players = get_players()

win = Tk()
game = GUI(win, players)
win.update_idletasks()
win.resizable(False, False)
win.mainloop()

# def get_players():
# players = []
# print("=" * 10)
# num = int(input("Number of Players: "))
# for i in range(num):
#     players.append(input(f"Name {i+1}: "))
# print("=" * 10)
# print("Starting game with: ", end="")
# print(*players, sep=", ", end="\n")
# print("=" * 10)
# return players

