from tkinter import Tk, Canvas
from moleopoly import Board


class Game(Board):
    def __init__(self, players: list):
        super().__init__(*players)


def get_players():
    players = []
    print("=" * 10)
    num = int(input("Number of Players: "))
    for i in range(num):
        players.append(input(f"Name {i+1}: "))
    print("=" * 10)
    print("Starting game with: ", end="")
    print(*players, sep=", ", end="\n")
    print("=" * 10)
    return players


game = Game(get_players())

# class GUI(Canvas):
#     WIDTH = 800
#     HEIGHT = 800

#     def __init__(self, root):
#         super().__init__(master=root, width=GUI.WIDTH, height=GUI.HEIGHT, bg="white")
#         self.root = root
#         self.pack()


# win = Tk()
# GUI(win)
# win.resizable(False, False)
# win.update_idletasks()
# win.mainloop()
