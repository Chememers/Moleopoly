from tkinter import  Frame, Tk, Canvas, Toplevel, Label, Button, Entry
from tkinter.constants import CENTER, E, NW, RIDGE, W, END
from moleopoly import Board, ElementSquare, Chance, Player, Utility
from const import SQLONG, SQSHORT, COLORS
from PIL import ImageTk, Image
from time import sleep

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
        self.color = "#CCCCCC"
        self.root = root
        self.config(
            bg=self.color,
            bd=0,
            highlightthickness=0.5,
            relief=RIDGE,
            highlightbackground="black",
        )
        self.text = text
        self.loc = loc
        size = 22
        if "Visiting" in text:
            size = 18
        self.create_text((SQSHORT, SQSHORT), text=text, font=Font(size), anchor=CENTER)
        self.row, self.col = self.put()

    def put(self):
        pairs = ((9, 0), (0, 0), (0, 9), (9, 9))
        row, col = pairs[self.loc]
        self.grid(row=row, column=col, columnspan=2)
        return (row, col)

    def rect_coords(self):
        return [self.row*75 + 50, self.col*75 + 50]

    def raise_window(self, player):
        if self.text == "Go!!":
            return
        win = Toplevel(self.root)
        win.config(bg=self.color)
        win.resizable(False, False)
        if "visit" in self.text.lower():
            win.title("Visiting Jail...")
            imgopen = Image.open(r"resources\Jail.jpg")
            imgtk = ImageTk.PhotoImage(imgopen)
            lbl = Label(win, image=imgtk)
            lbl.image = imgtk

            fee = 10000
            player.balance -= fee
            Label(win, text=f"Visiting Jail...Entry fee = {fee}!", bg="white", font=Font(20)).grid(row=0, column=0, sticky="we")
            lbl.grid(row=1, column=0, sticky="we")
        elif "jail" in self.text.lower():
            win.title("GO TO JAIL!")
            imgopen = Image.open(r"resources\Go to Jail.jpg")
            imgtk = ImageTk.PhotoImage(imgopen)
            lbl = Label(win, image=imgtk)
            lbl.image = imgtk
            Label(win, text=f"{player.name} going to jail for 3 turns!!", bg="white", font=Font(20)).grid(row=0, column=0, sticky="we")
            lbl.grid(row=1, column=0, sticky="we")
        else:
            win.title("MOLE HOLE!")
            imgopen = Image.open(r"resources\Mole Hole.png").resize((640, 360), Image.ANTIALIAS)
            imgtk = ImageTk.PhotoImage(imgopen)
            lbl = Label(win, image=imgtk)
            lbl.image = imgtk
            Label(win, text=f"Welcome to the Mole Hole!", bg="white", font=Font(20)).grid(row=0, column=0, sticky="we")
            lbl.grid(row=1, column=0, sticky="we")

        win.mainloop()


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
        self.root = master
        self.children = set()
        self.win = master
        self.side = side
        self.idx = index

    def add_child(self, data):
        self.children.add(data)

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
            for text in self.children:
                text.angle = 180
                text.location = (SQLONG - text.location[0], SQSHORT - text.location[1])
        else:
            self.canv_config["width"] = SQSHORT
            self.canv_config["height"] = SQLONG
            for text in self.children:
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
        for item in self.children:
            item.draw(self.canv)
        
    def setup(self):
        raise NotImplementedError("Must implement setup method")

    def raise_window(self, player):
        raise NotImplementedError()

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
        self.root = master
        self.grp = int(self.square.Group)
        if self.grp > 10:
            self.grp -= 10
        self.canv_config["bg"] = self.COLORS[self.grp]
        self.setup()
        self.grid_criteria()
        self.put()

    def setup(self):
        self.add_child(Text(self.square.Symbol, (SQSHORT, 35), 32))
        self.add_child(Text(f"{round(float(self.square.AtomicNumber))}", (SQSHORT, 62), 12))
        self.add_child(Text(self.square.Element, (SQSHORT, 12), 12))

    def raise_window(self, player):
        win = Toplevel(self.root)
        win.geometry("500x200")
        bg = self.COLORS[self.grp]

        def close():
            win.destroy()
        
        def buy():
            self.square.sell(player)
            close()

        c = Frame(win, width=500, height=200, bg = bg)
        Label(c, text=f"NAME: {self.square.Element}, # {int(self.square.AtomicNumber)}", font = Font(18), bg = bg).place(x=250, y = 20, anchor=CENTER)
        Label(c, text=f"DISCOVERER: {self.square.Discoverer}, {self.square.Year}", font = Font(18), bg = bg).place(x=250, y = 52, anchor=CENTER)
        Label(c, text=f"PRICE: {self.square.price} KJ", font = Font(18), bg = bg).place(x=250, y = 84, anchor=CENTER)
        
        if self.square.owned_by is None:
            win.title(f"Buy {self.square.Element}?")
            Label(c, text="Do you want to Buy?", font = Font(18), bg = bg).place(x = 250, y = 115, anchor=CENTER)
            Button(c, text="Yes", bg="green", fg="white", font = Font(12), width = 20, height = 1, command=buy).place(x = 145, y = 170, anchor=CENTER)
            Button(c, text="No", bg="red", fg="white", font = Font(12), width = 20, height = 1, command=close).place(x = 345, y = 170, anchor=CENTER)
 
        else:
            message = f"This is your property, {player.name}"
            if self.square.owned_by.name != player.name:
                player.balance -= self.square.rent
                self.square.owned_by.balance += self.square.rent
                win.title(f"Pay energy to {self.square.owned_by.name}") 
                message = f"You have paid energy to {self.square.owned_by.name}"

            Label(c, text=f"NAME: {self.square.Element}, # {int(self.square.AtomicNumber)}", font = Font(18), bg = bg).place(x=250, y = 20, anchor=CENTER)
            Label(c, text=f"DISCOVERER: {self.square.Discoverer}, {self.square.Year}", font = Font(18), bg = bg).place(x=250, y = 52, anchor=CENTER)
            Label(c, text=f"PRICE: {self.square.price} KJ", font = Font(18), bg = bg).place(x=250, y = 84, anchor=CENTER)  
            Label(c, text=message, font = Font(18), bg = bg).place(x = 250, y = 115, anchor=CENTER)
            Button(c, text="OK", bg="blue", fg="white", font = Font(12), width = 20, height = 1, command=close).place(x = 250, y = 170, anchor=CENTER)
            

        c.place(x = 0, y = 0)
        win.mainloop()
        return

class ChanceGUI(SquareGUI):
    def __init__(self, master, square: Chance, side, idx):
        super().__init__(master, side, idx)

        self.square = square
        self.canv_config["bg"] = "#cfe0fa"
        self.setup()
        self.grid_criteria(allRotate=True)
        self.put()

    def setup(self):
        self.add_child(Text("?", (SQSHORT, 35), 50, "orange"))

    def raise_window(self, player):
        imgFile = ImageTk.PhotoImage(Image.open(r"resources\chance.jpg"))
        win = Toplevel(self.root)
        win.geometry("550x550")
        win.title(f"Test for you, {player.name}")
        Label(win, image=imgFile).place(x = 0, y = 0)

        qa = self.square.random_question()
        q = qa[0]; a = qa[1]

        def close():
            win.destroy()
   
        Label(win, text=q, font=Font(18),  wraplengt=400).place(x = 275, y = 80, anchor=CENTER)
        e = Entry(win, font=Font(18))
        e.place(x = 275, y = 475, width=300, height = 40, anchor=CENTER)
        e.insert(END, "Answer")
        
        def verify_ans():
            if e.get() == a:
                Label(win, text="Correct! +1000 KJ", font = Font(36), fg="green").place(relx = 0.5, rely= 0.5, anchor=CENTER)
                player.balance += 1000
            else:
                Label(win, text="Incorrect. -500 KJ", font = Font(36), fg="red").place(relx = 0.5, rely= 0.5, anchor=CENTER)
                player.balance -= 500

            Button(win, text="OK!", bg="blue", fg="white", font = Font(18), width = 24, height = 1, command=close).place(relx = 0.5, rely = 0.7, anchor=CENTER)

        Button(win, text="OK", bg="blue", fg="white", font = Font(12), width = 20, height = 1, command=verify_ans).place(x = 275, y = 525, anchor=CENTER)
        win.mainloop()

        return


class UtilityGUI(SquareGUI):
    def __init__(self, master, square: Utility, side, idx):
        super().__init__(master, side, idx)

        self.square = square
        self.color = "#ede59d"
        self.canv_config["bg"] = self.color
        self.setup()
        self.grid_criteria()
        self.put()

    def setup(self):
        size = 24 if self.square.name == "Buret" else 12
        self.add_child(Text(self.square.name, (SQSHORT, 35), size))

    def raise_window(self, player):
        win = Toplevel(self.root)
        win.geometry("600x550")
        win.config(bg=self.color)
        name = self.square.name
        ext = ".jpg" if "Burn" in name or "Scale" in name else ".png"
        imgFile = ImageTk.PhotoImage(Image.open(fr"utils\{name}{ext}"))
        def close():
            win.destroy()
        
        def buy():
            self.square.sell(player)
            close()
        
        if self.square.owned_by is None:
            Label(win, text=f"Utility - {name}!", bg=self.color, font=Font(20)).grid(row=0, column=0, sticky="we")
            img = Label(win, image=imgFile)
            img.image = imgFile
            img.grid(row=1, column=0, sticky="we")
            Button(win, text="Buy!", bg="green", font=Font(15),command=buy).grid(row=2, column=0, sticky="we")
            win.update_idletasks()
        else:
            print(self.square.owned_by)

        win.mainloop()
        return

class InfoDisplay(Canvas):
    def __init__(self, master, players):
        super().__init__(master, bg="#D0B0D0", width=460, height=120)
        self.config(
            highlightthickness=0.5, highlightbackground="black",
        )
        self.players = players
        self.update(0)

    def update(self, turn):
        self.delete("all")
        for i in range(len(self.players)):
            if i < 2: x = 50; col = i + 1
            else: x = 275; col = i - 1
            rx = x - 30
            ry = x - 10

            self.create_rectangle(rx, col * 35, ry, (col * 35) + 20, fill=COLORS[i])
            self.create_text((x, (col) * 35 + 10),text=self.players[i].name,fill="white",font=Font(12),anchor=W)
            self.create_text((x + 170, (col) * 35 + 10),text=(f"{self.players[i].balance} KJ"),fill="white",font=Font(12),anchor=E)

        # Show Active Player:
        x, y = (45, 30); w = 180; h = 35
        if turn > 1: x += 225
        if turn % 2 != 0: y += 35

        self.create_rectangle(x, y, x + w, y + h, outline="#9BF62E", width=3)


class Piece(Player):
    def __init__(self, master, boxes, name: str, turn) -> None:
        super().__init__(name, turn)
        self.boxes = boxes
        self.win = master
        self.turn = turn
        self.color = COLORS[self.turn]
        self.canv = Canvas(self.win)
        self.loc = self.coord()
        self.jailed =  False
        self.jailCount = 0
        self.draw()

    def coord(self):
        pos = self.boxes[self.position].rect_coords()
        if self.position // 9 % 2 == 0:
            pos[1] += self.turn*25
        else:
            pos[0] += self.turn*25
        return pos
    
    def draw(self):
        pos = self.coord()
        self.canv.place_forget()
        self.canv = Canvas(self.win, bg = self.color, width=20, height=20)
        self.canv.place(x = pos[1], y = pos[0])

    def move_callback(self, i, steps):
        if i == steps:
            self.boxes[self.position].raise_window(self)
            return
        self.position += 1
        if self.position == 32:
            self.position = 0
            self.balance += 10000
        self.draw()
        self.win.after(250, lambda: self.move_callback(i+1, steps))

    def move(self, steps):
        if not self.jailed:
            self.move_callback(0, steps)
        if self.position == 17:
            pos = self.boxes[8].rect_coords()
            if self.position // 9 % 2 == 0:
                pos[1] += self.turn*25
            else:
                pos[0] += self.turn*25
            self.canv.place_forget()
            self.canv = Canvas(self.win, bg = self.color, width=20, height=20)
            self.canv.place(x = pos[1], y = pos[0])
            self.jailed = True
        if self.jailed:
            self.jailCount += 1
            if self.jailCount == 3:
                self.jailCount = 0
                self.jailed = False


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
        self.center.bind("<Button-1>", self.playturn)

        self.pieces = [Piece(self.win, self.boxes, player.name, player.turn) for player in self.players]
        self.info = InfoDisplay(self.win, self.pieces)
        self.info.place(x=180, y=250, anchor=NW)

        self.center.create_rectangle((150, 300, 350, 400), fill="#bdecb6", outline="black", width=3)
        self.update_dice(1, 1) 

    def game_over(self):
        for player in self.pieces:
            if player.balance >= 200000000:
                return True
        return False
    
    def playturn(self, event):
        a, b, c = self.pieces[self.turn].roll_die()
        self.update_dice(a, b)
        self.pieces[self.turn].move(c) # c
        self.turn += 1; self.turn %= len(self.pieces)
        self.info.update(self.turn)
        if self.game_over():
            self.center.bind("<Button-1>", lambda e: None)
            self.center.create_text((250, 450), text=f"GAME OVER!\n{self.pieces[self.turn].name} won the game!", font=Font(40), anchor=CENTER)
                
    def update_dice(self, a, b):
        self.win.img1 = img1 = ImageTk.PhotoImage(Image.open(fr"dice\dice_{a}.png"))
        self.win.img2 = img2 = ImageTk.PhotoImage(Image.open(fr"dice\dice_{b}.png"))
        self.center.create_image((250, 350), image=img1, anchor=E)
        self.center.create_image((250, 350), image=img2, anchor=W)

def run(players):
    win = Tk()
    win.config(bg="#bdecb6")
    win.resizable(False, False)
    GUI(win, players)
    win.update_idletasks()
    win.mainloop()


if __name__ == "__main__":
    players = ("Aditya", "Gowtham")
    run(players)

