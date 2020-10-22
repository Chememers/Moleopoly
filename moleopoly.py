from random import randint
from chemlib import pte, Element
 
class Board:
    def __init__(self, *args):
        self.players = [Player(name) for name in args]

        self.squares = set()

        while len(self.squares) < 20:
            self.squares.add(randint(1, 100))

        self.squares = sorted(list(self.squares))
        self.board = ["Go"] + self.squares
        self.board.insert(4, Utility("Bunsen Burner"))
        self.board.insert(7, Chance())
        self.board.insert(8, "Jail")
        self.board.insert(12, Utility("Graduated Cylinder"))
        self.board.insert(13, Chance())
        self.board.insert(16, "Go Again")
        self.board.insert(20, Utility("Buret"))
        self.board.insert(23, Chance())
        self.board.insert(24, "Go To Jail")
        self.board.insert(28, Utility("Weight Scale"))
        self.board.insert(29, Chance())

        for i in range(len(self.board)):
            if type(self.board[i]) is int:
                self.board[i] = ElementSquare(self.board[i])

class ElementSquare(Element):
    def __init__(self, atomic_number):
        sym = list(pte["Symbol"])
        super(ElementSquare, self).__init__(sym[atomic_number - 1])
        self.owned_by = None
        self.houses = []

class Utility:
    def __init__(self, name):
        self.starting_price = 200
        self.bidders = {}
        self.current_price = 200
        self.name = name

class Chance:
    def __init__(self):
        pass

class Player:
    def __init__(self, name):
        self.name = name
        self.position = 0
        self.doubles = False
        self.owned_elements = []
        self.balance = 100000 #starting balance, in Joules
    
    def roll_die(self):
        a = randint(1, 6)
        b = randint(1, 6)
        if a == b:
            self.doubles = True
        else:
            self.doubles = False
        return a + b
        
    def move(self):
        self.position += self.roll_die()
        if self.position >= 31:
            self.position -= 31
            self.currency += 10000
 
if __name__ == "__main__":
    p1 = Player("Gowtham")
 
    b = Board(p1)
    print(b.players)
    print(b.squares)
    print(b.board)
    print(b.board[1].FirstIonization)
