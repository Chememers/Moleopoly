from tkinter import  Tk, Canvas
from tkinter.constants import CENTER, E, NW, RIDGE, W
from moleopoly import Board, ElementSquare, Chance, Player, Utility
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
        self.rect_coords = (65, 65, 85, 85)
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
            self.rotate(270)
            self.grid_config["row"] = 0
            self.grid_config["column"] = self.idx + 2
            self.grid_config["rowspan"] = 2
        else:
            self.rotate(90)
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
                if angle == 270:
                    text.location = (SQSHORT - text.location[1], text.location[0])
                else:
                    text.location = (text.location[1], text.location[0])

    def rect_coords(self):
        return [self.grid_config["row"] * 75 + 50, self.grid_config["column"]*75+50]

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
        self.add_child("txt", Text(self.square.Symbol, (SQSHORT, 35), 32))
        self.add_child(
            "txt", Text(f"{round(float(self.square.AtomicNumber))}", (SQSHORT, 62), 12)
        )
        self.add_child("txt", Text(self.square.Element, (SQSHORT, 12), 12))


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
        size = 24 if self.square.name == "Buret" else 12
        self.add_child("txt", Text(self.square.name, (SQSHORT, 35), size))


class InfoDisplay(Canvas):
    def __init__(self, master, players):
        super().__init__(master, bg="#D0B0D0", width=460, height=120)
        self.config(
            highlightthickness=0.5, highlightbackground="black",
        )
        self.players = players
        self.colors = ["red", "green", "blue", "yellow"]
        self.update(0)

    def update(self, turn):
        self.delete("all")
        for i in range(len(self.players)):
            if i < 2: x = 50; col = i + 1
            else: x = 275; col = i - 1
            rx = x - 30
            ry = x - 10

            self.create_rectangle(rx, col * 35, ry, (col * 35) + 20, fill=self.colors[i])
            self.create_text((x, (col) * 35 + 10),text=self.players[i].name,fill="white",font=Font(12),anchor=W)
            self.create_text((x + 170, (col) * 35 + 10),text=(f"{self.players[i].balance} KJ"),fill="white",font=Font(12),anchor=E)

        # Show Active Player:
        x, y = (45, 30); w = 180; h = 35
        if turn > 1: x += 225
        if turn % 2 != 0: y += 35

        self.create_rectangle(x, y, x + w, y + h, outline="#9BF62E", width=3)


class Piece(Player):
    def __init__(self, boxes, name: str) -> None:
        super().__init__(name)
        self.boxes = boxes
    
    def coord(self):
        pos = self.boxes[self.position]
    
    def draw(self):
        x = self.coord()["x"]; y = self.coord()["y"]
        self.canv = Canvas(self.win, bg = "red", width=20, height=20)
        self.canv.place(x = x, y = y)
        #self.win.create_rectangle(x, y, x+10, y+10)

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
            for j in range(*ranges[i]):
                args = (self.win, self.board[j], dirs[i], j - ranges[i][0])
                if isinstance(self.board[j], ElementSquare):
                    self.boxes[j] = ElementSquareGUI(*args)
                elif isinstance(self.board[j], Chance):
                    self.boxes[j] = ChanceGUI(*args)
                elif isinstance(self.board[j], Utility):
                    self.boxes[j] = UtilityGUI(*args)

        # player position = 10
        # self.boxes[10].rect_position()

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

        p = Piece(self, self.current_player())

        p.draw()
        for i in range(10):
            input()
            p.position += 1
            p.draw()


def run(players):
    win = Tk()
    win.config(bg="#bdecb6")
    win.resizable(False, False)
    GUI(win, players)
    win.update_idletasks()
    win.mainloop()


if __name__ == "__main__":
    players = ("Aditya", "Gowtham", "Hari")
    run(players)

