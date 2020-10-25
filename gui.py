from tkinter import Tk, Frame, Canvas
from tkinter.constants import BOTH, CENTER, NW, RIDGE
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
        self.canv = Canvas(
            self,
            bg="#bdecb6",
            width=145,
            height=145,
            bd=0,
            highlightthickness=0,
            relief=RIDGE,
        )
        self.canv.place(x=3, y=3)
        self.canv.create_text((70, 70), text=self.text, font=Font(25), anchor=CENTER)

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
                (70, 32),
                text=self.square.Symbol,
                fill="black",
                anchor=CENTER,
                font=Font(32),
            )
            self.canv.create_text(
                (70, 58),
                text=f"{round(float(self.square.AtomicNumber))}",
                fill="#555555",
                anchor=CENTER,
                font=Font(12),
            )
            self.canv.create_text(
                (70, 8),
                text=self.square.Element,
                fill="#555555",
                anchor=CENTER,
                font=Font(12),
                # angle=angle,
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
                (33, 70),
                text=self.square.Symbol,
                fill="black",
                anchor=CENTER,
                font=Font(32),
                angle=angle,
            )
            self.canv.create_text(
                (8, 70),
                text=self.square.Element,
                fill="#555555",
                anchor=CENTER,
                font=Font(12),
                angle=angle,
            )
            self.canv.create_text(
                (58, 70),
                text=f"{round(float(self.square.AtomicNumber))}",
                fill="#555555",
                anchor=CENTER,
                font=Font(12),
                angle=angle,
            )


class ChanceGUI(SquareGUI):
    def __init__(self, master, square: Chance, side, idx):
        super().__init__(master, side, idx)

        self.square = square
        self.setup()
        self.put()

    def setup(self):
        angles = {"S": 0, "W": 90, "N": 180, "E": 270}
        if self.orient == "H":
            self.canv = Canvas(
                self.frame,
                bg="white",
                width=140,
                height=65,
                bd=0,
                highlightthickness=0,
                relief=RIDGE,
            )
            pos = (70, 30)
        else:
            self.canv = Canvas(
                self.frame,
                bg="white",
                width=65,
                height=140,
                bd=0,
                highlightthickness=0,
                relief=RIDGE,
            )
            pos = (30, 70)

        self.canv.place(x=3, y=3)
        self.canv.create_text(
            pos,
            text="?",
            font=Font(50),
            fill="orange",
            anchor=CENTER,
            angle=angles[self.side],
        )


class UtilityGUI(SquareGUI):
    def __init__(self, master, square: Utility, side, idx):
        super().__init__(master, side, idx)

        self.square = square
        self.color = "white"
        self.setup()
        self.put()

    def setup(self):
        if self.square.name == "Buret":
            size = 24
        else:
            size = 12
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
                (70, 30),
                text=self.square.name,
                fill="black",
                anchor=CENTER,
                font=Font(size),
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
                (30, 70),
                text=self.square.name,
                fill="black",
                anchor=CENTER,
                font=Font(size),
                angle=angle,
            )


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

        self.center = Canvas(self.win, bg="#bdecb6", width=500, height=500)
        self.center.place(x=160, y=160, anchor=NW)
        self.center.create_text(
            (250, 250), text="Mole-O-Poly", anchor=CENTER, font=Font(50)
        )


if __name__ == "__main__":
    players = ("Aditya", "Gowtham", "Hari")
    win = Tk()
    win.config(bg="#bdecb6")
    win.geometry(f"{SIZE}x{SIZE}")
    win.resizable(False, False)
    game = GUI(win, players)
    win.mainloop()
