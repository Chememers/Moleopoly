from random import randint, choice
from chemlib import pte, Element
import pandas as pd

Group1 = [1] + [choice([3, 11, 19]), choice([37, 55])]
Group2 = [4] + [choice([12, 20, 38])]
Group3 = [5] + [choice([13, 31]), 49]
Group4 = [6] + [choice([14, 32, 50])]
Group5 = [7] + [choice([15, 33]), choice([51, 83])]
Group6 = [8] + [choice([16, 34, 42])]
Group7 = [9] + [choice([17, 35]), choice([53, 85])]
Group8 = [2] + [choice([10, 18, 36, 54, 86])]

class ElementSquare(Element):
    def __init__(self, atomic_number):
        sym = list(pte["Symbol"])
        super(ElementSquare, self).__init__(sym[atomic_number - 1])
        self.owned_by = None
        self.houses = []
        self.price = round((float(self.FirstIonization)/9.223e+18)*6.02e23)
        self.rent = round(self.price*3/4)
    
    def sell(self, buyer):
        buyer.balance -= self.price
        self.owned_by = buyer


class Utility:
    def __init__(self, name):
        self.starting_price = 200
        self.owned_by = None
        self.current_price = 200
        self.name = name

    def sell(self, buyer):
        buyer.balance -= self.current_price
        self.owned_by = buyer

class Chance:
    pass
    # qa = pd.read_csv(r"resources\Questions.csv")

    # @classmethod
    # def get_question(cls):
    #     idx = cls.qa.shape[0]

    #     return cls.qa

    # def random_question():
    #     rando = randint(0, len(questions) - 1)
    #     return {questions[rando]: answers[rando]}

board = (
    ["Go!!"]
    + Group1
    + [Utility("Bunsen Burner")]
    + Group2
    + [Chance(), "Visiting Jail..."]
    + Group3
    + [Utility("Graduated Cylinder"), Chance()]
    + Group4
    + ["Mole Hole!"]
    + Group5
    + [Utility("Buret")]
    + Group6
    + [Chance(), "Go to Jail!"]
    + Group7
    + [Utility("Weight Scale"), Chance()]
    + Group8
)

df = pd.read_csv(r"resources\Questions.csv")
questions = list(df["Question"])
answers = list(df["Answer"])


class Board:
    def __init__(self, *args):
        self.players = []
        for i in range(len(args)):
            self.players.append(Player(args[i], i))

        #self.players = [Player(name) for name in args]
        self.turn = 0

        self.board = board

        for i in range(len(self.board)):
            if type(self.board[i]) is int:
                self.board[i] = ElementSquare(self.board[i])

    def current_player(self):
        return self.players[self.turn]


class Player:
    def __init__(self, name, turn):
        self.name = name
        self.position = 0
        self.doubles = False
        self.owned_elements = []
        self.balance = 5000000  # starting balance, in Joules
        self.turn = turn

    def roll_die(self):
        a = randint(1, 6)
        b = randint(1, 6)
        if a == b:
            self.doubles = True
        else:
            self.doubles = False
        return (a, b, a + b)

    # def increment(self):
    #     self.position += self.roll_die()[2]
    #     if self.position >= 31:
    #         self.position -= 31
    #         self.balance += 10000


if __name__ == "__main__":
    p1 = Player("Gowtham", 1)

    b = Board(p1)
    print(b.board)
    print(len(b.board))

    print(b.board)
