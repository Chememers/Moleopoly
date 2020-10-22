from random import randint
from chemlib import pte, Element
 
class Board:
    def __init__(self, players):
        self.squares = set()
        while len(self.squares) < 20:
            self.squares.add(randint(1, 100))
        self.squares = sorted(list(self.squares))
        self.players = players
        self.board = self.squares

class ElementSquare(Element):
    def __init__(self, atomic_number):
        sym = list(pte["Symbol"])
        super(ElementSquare, self).__init__(sym[atomic_number - 1])
        self.owned_by = None
        self.houses = []

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
        if self.position > 30:
            self.position -= 30
            self.currency += 10000
 
if __name__ == "__main__":
    p1 = Player("Gowtham")
 
    b = Board([p1])
    print(b.squares)

    e = ElementSquare(1)
    print(e.AtomicNumber)
