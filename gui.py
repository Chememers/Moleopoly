from tkinter import Tk, Frame, Canvas
from tkinter.constants import BOTH, CENTER, RIDGE
from moleopoly import Board, ElementSquare, Chance, Utility
from const import SIZE

# fill="#74BBFB"


def Font(size):
    return ("Calibri", size, "bold")


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
        if self.side == "W" or self.side == "E":
            self.orient = "H"
        else:
            self.orient = "V"
        self.idx = index

        self.frame = Frame(
            master, bg="#FFFFFF", highlightbackground="black", highlightthickness=1
        )

    def put(self):
        if self.orient == "H":
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
    COLORS = (
        None,
        "#51c447",
        "#7beb71",
        "#8ab0e6",
        "#c187ff",
        "#f7a659",
        "#f0f266",
        "#f06565",
        "#ababab",
    )

    def __init__(self, master, square: ElementSquare, side, idx):
        super().__init__(master, side, idx)
        self.square = square
        grp = int(self.square.Group)
        if grp > 10:
            grp -= 10
        self.color = self.COLORS[grp]
        self.frame.config(bg=self.color)

        self.setup()
        self.put()

    def setup(self):
        if self.orient == "H":
            self.canv = Canvas(
                self.frame,
                bg=self.color,
                width=140,
                height=65,
                bd=0,
                highlightthickness=0,
                relief=RIDGE,
            )
            self.canv.place(x=3, y=3)
            self.canv.create_text(
                (70, 40),
                text=self.square.Symbol,
                fill="black",
                anchor=CENTER,
                font=Font(32),
            )
            self.canv.create_text(
                (70, 10), text="Element", fill="#555555", anchor=CENTER, font=Font(12),
            )
        else:
            angle = 270 if self.side == "N" else 90
            self.canv = Canvas(
                self.frame,
                bg=self.color,
                width=65,
                height=140,
                bd=0,
                highlightthickness=0,
                relief=RIDGE,
            )
            self.canv.place(x=3, y=3)
            self.canv.create_text(
                (40, 70),
                text=self.square.Symbol,
                fill="black",
                anchor=CENTER,
                font=Font(32),
                angle=angle,
            )
            self.canv.create_text(
                (10, 70),
                text="Element",
                fill="#555555",
                anchor=CENTER,
                font=Font(12),
                angle=angle,
            )


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
