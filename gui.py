from tkinter import Tk, Frame
from tkinter.constants import BOTH
from moleopoly import Board, ElementSquare, Chance, Utility
from const import CENTERSIZE, SIZE, SQSHORT, SQLONG

# fill="#74BBFB"


class Corner(Frame):
    def __init__(self, root, text, loc):
        super().__init__(master=root, bg="#CCCCCC", height=150, width=150)
        self.config(highlightbackground="black", highlightthickness=1)
        self.text = text
        self.loc = loc
        self.put()

    def put(self):
        pairs = ((9, 0), (0, 0), (0, 9), (9, 9))
        row, col = pairs[self.loc]
        self.grid(row=row, column=col, columnspan=2)


class SquareGUI:
    def __init__(self, master, side, index):
        self.win = master
        self.side = side
        self.idx = index

        self.frame = Frame(
            master, bg="#FFFFFF", highlightbackground="black", highlightthickness=1
        )

    def put(self):
        if self.side == "W" or self.side == "E":
            self.frame.config(width=150, height=75)
            if self.side == "W":
                self.frame.grid(row=8 - self.idx, column=0, columnspan=2)
            else:
                self.frame.grid(row=self.idx + 2, column=9, columnspan=2)
        else:
            self.frame.config(width=75, height=150)
            if self.side == "N":
                self.frame.grid(row=0, column=self.idx + 2, rowspan=2)
            else:
                self.frame.grid(row=9, column=8 - self.idx, rowspan=2)


class ElementSquareGUI(SquareGUI):
    def __init__(self, master, square: ElementSquare, side, idx):
        super().__init__(master, side, idx)

        self.square = square
        self.put()


class ChanceGUI(SquareGUI):
    def __init__(self, master, square: Chance, side, idx):
        super().__init__(master, side, idx)

        self.square = square
        self.put()


class UtilityGUI(SquareGUI):
    def __init__(self, master, square: Utility, side, idx):
        super().__init__(master, side, idx)

        self.square = square
        self.put()


class GUI(Board):
    def __init__(self, master, players: list):
        super().__init__(*players)
        self.win = master
        self.boxes = [None for _ in range(32)]
        self.setup_board()

    def setup_board(self):
        for i in range(0, len(self.board), 8):
            self.boxes[i] = Corner(self.win, self.board[i], i // 8)

        dirs = ("W", "N", "E", "S")
        ranges = ((1, 8), (9, 16), (17, 24), (25, 32))

        for i in range(4):
            index = 0
            for j in range(*ranges[i]):
                if isinstance(self.board[j], ElementSquare):
                    self.boxes[j] = ElementSquareGUI(
                        self.win, self.board[j], dirs[i], index
                    )
                elif isinstance(self.board[j], Chance):
                    self.boxes[j] = ChanceGUI(self.win, self.board[j], dirs[i], index)
                elif isinstance(self.board[j], Utility):
                    self.boxes[j] = UtilityGUI(self.win, self.board[j], dirs[i], index)
                index += 1

        # for i in range(2, 9):
        #     Frame(
        #         self.win,
        #         width=75,
        #         height=150,
        #         highlightbackground="black",
        #         highlightthickness=1,
        #     ).grid(row=0, column=i, rowspan=2)


players = ("Aditya", "Gowtham", "Hari")


win = Tk()
win.geometry(f"{SIZE}x{SIZE}")
win.resizable(False, False)
game = GUI(win, players)
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

# players = get_players()

# dirs = ("W", "N", "E", "S")
# ranges = ((1, 8), (9, 16), (17, 24), (25, 32))
# for i in range(4):
#     for j in range(*ranges[i]):
#         sq = self.squares[j]
#         if isinstance(sq, ElementSquare):
#             ElementSquareGUI(self.canvas, sq, dirs[i])
