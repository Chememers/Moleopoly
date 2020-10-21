from random import randint
import tkinter as tk
 
class Board:
    def __init__(self, players):
        self.squares = set()
        while len(self.squares) < 30:
            self.squares.add(randint(1, 100))
        self.squares = sorted(list(self.squares))
        self.players = players
 
class Player:
    def __init__(self, name):
        self.name = name
        self.position = 0
        self.doubles = False
    
    def roll_die(self):
        a = randint(1, 6)
        b = randint(1, 6)
        if a == b:
            self.doubles = True # add later best
        else:
            self.doubles = False
        return a + b
        
    def move(self):
        self.position += self.roll_die()
 
if __name__ == "__main__":
    p1 = Player("Gowtham")
 
    b = Board([p1])
    print(b.squares)
