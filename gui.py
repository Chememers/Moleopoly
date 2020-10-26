from tkinter import Tk, Canvas
from tkinter.constants import CENTER, NW, RIDGE
from moleopoly import Board, ElementSquare, Chance, Utility
from const import SQLONG, SQSHORT


def Font(size):
    return ("Calibri", size, "bold")


class Text:
    def __init__(self, text, location, size, color="black"):
        self.text = text
        self.location = location
        self.angle = 0
        self.size = size
        self.color = color

    def draw(self, canv: Canvas):
        canv.create_text(
            self.location,
            text=self.text,
            fill=self.color,
            font=Font(self.size),
            anchor=CENTER,
            angle=self.angle,
        )


class Corner(Canvas):
    def __init__(self, root, text, loc):
        super().__init__(root, height=SQLONG, width=SQLONG)
        self.config(
            bg="#CCCCCC",
            bd=0,
            highlightthickness=0.5,
            relief=RIDGE,
            highlightbackground="black",
        )
        self.text = text
        self.loc = loc
        self.create_text((SQSHORT, SQSHORT), text=text, font=Font(25), anchor=CENTER)
        self.put()

    def put(self):
        pairs = ((9, 0), (0, 0), (0, 9), (9, 9))
        row, col = pairs[self.loc]
        self.grid(row=row, column=col, columnspan=2)


class SquareGUI:
    def __init__(self, master, side, index):
        self.grid_config = {}
        self.canv_config = {
            "width": SQLONG,
            "height": SQSHORT,
            "bg": "#FFFFFF",
            "highlightbackground": "black",
            "highlightthickness": 0.5,
            "relief": RIDGE,
        }
        # DEFAULT TO WEST EAST, ROTATE WILL MUTATE
        self.children = {"txt": set()}
        self.win = master
        self.side = side
        self.idx = index

    def add_child(self, type_, data):
        self.children[type_].add(data)

    def grid_criteria(self, allRotate=False):
        if self.side == "W":
            self.grid_config["row"] = 8 - self.idx
            self.grid_config["column"] = 0
            self.grid_config["columnspan"] = 2
        elif self.side == "E":
            if allRotate:
                self.rotate(180)
            self.grid_config["row"] = self.idx + 2
            self.grid_config["column"] = 9
            self.grid_config["columnspan"] = 2
        elif self.side == "N":
            self.rotate(90)
            self.grid_config["row"] = 0
            self.grid_config["column"] = self.idx + 2
            self.grid_config["rowspan"] = 2
        else:
            self.rotate(270)
            self.grid_config["row"] = 9
            self.grid_config["column"] = 8 - self.idx
            self.grid_config["rowspan"] = 2

    def rotate(self, angle):
        if angle == 180:
            for text in self.children["txt"]:
                text.angle = 180
                text.location = (SQLONG - text.location[0], SQSHORT - text.location[1])
        else:
            self.canv_config["width"] = SQSHORT
            self.canv_config["height"] = SQLONG
            for text in self.children["txt"]:
                text.angle = angle
                if angle == 90:
                    text.location = (SQSHORT - text.location[1], text.location[0])
                else:
                    text.location = (text.location[1], text.location[0])

    def put(self):
        self.canv = Canvas(self.win, **self.canv_config)
        self.canv.grid(**self.grid_config)
        for key in self.children:
            for item in self.children[key]:
                item.draw(self.canv)

    def setup(self):
        raise NotImplementedError("Must implement setup method")


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
        self.canv_config["bg"] = self.COLORS[grp]
        self.setup()
        self.grid_criteria()
        self.put()

    def setup(self):
        self.add_child("txt", Text(self.square.Symbol, (SQSHORT, 32), 32))
        self.add_child(
            "txt", Text(f"{round(float(self.square.AtomicNumber))}", (SQSHORT, 58), 12)
        )
        self.add_child("txt", Text(self.square.Element, (SQSHORT, 8), 12))


class ChanceGUI(SquareGUI):
    def __init__(self, master, square: Chance, side, idx):
        super().__init__(master, side, idx)

        self.square = square
        self.setup()
        self.grid_criteria(allRotate=True)
        self.put()

    def setup(self):
        self.add_child("txt", Text("?", (SQSHORT, 35), 50, "orange"))


class UtilityGUI(SquareGUI):
    def __init__(self, master, square: Utility, side, idx):
        super().__init__(master, side, idx)

        self.square = square
        self.setup()
        self.grid_criteria()
        self.put()

    def setup(self):
        if self.square.name == "Buret":
            size = 24
        else:
            size = 12
        self.add_child("txt", Text(self.square.name, (SQSHORT, 30), size))


class InfoDisplay(Canvas):
    def __init__(self, master, players):
        super().__init__(bg="#D0B0D0", width=460, height=120)
        self.config(
            highlightthickness=0.5, highlightbackground="black",
        )
        colors = ["red", "green", "blue", "yellow"]

        for i in range(len(players)):
            if i < 2: x = 50; col = i + 1 
            else: x = 250; col = i - 1
            rx = x - 30; ry = x-10

            self.create_rectangle(rx, col*35, ry, (col*35) + 20, fill=colors[i])
            self.create_text((x, (col) * 35 + 10), text=players[i].name, fill="white", font=Font(12), anchor="w")
            self.create_text((x + 190, (col) * 35 + 10), text=players[i].balance, fill="white", font=Font(12), anchor="e")


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

        self.center = Canvas(
            self.win,
            bg="#bdecb6",
            width=500,
            height=500,
            highlightthickness=0.5,
            highlightbackground="black",
        )
        self.center.place(x=160, y=160, anchor=NW)
        self.center.create_text(
            (250, 40), text="Mole-O-Poly", anchor=CENTER, font=Font(50)
        )
        self.info = InfoDisplay(self.win, self.players)
        self.info.place(x=180, y=250, anchor=NW)


if __name__ == "__main__":
    players = ("Aditya", "Gowtham", "Hari", "W")
    win = Tk()
    win.config(bg="#bdecb6")
    win.resizable(False, False)
    game = GUI(win, players)
    win.update_idletasks()
    win.mainloop()
