from gui import GUI
from const import SIZE
from tkinter import Tk

import PySimpleGUI as sg

sg.theme('DarkGreen1')   

players = []

layout = [  [sg.Text('New Game', font=('Comic Sans MS', 20))],
            [sg.InputText(key="Name"), sg.Button('Add Player')],
            [sg.Text('Players:', font=('Comic Sans MS', 20))],
            [sg.Listbox(values=players, key="players", size=(30, 6))],
            [sg.Button('Play!'), sg.Button('Cancel')] ]

window = sg.Window('Mole-O-Poly', layout, element_justification="c")

cont = False
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel':
        cont = False
        break
    if event in ("Add Player"):
        players.append(values["Name"])
        window.Element('players').Update(values=players)
    if event in ("Play!") and len(players) > 0:
        cont = True
        break

if cont == True:
    window.close()

    players = ("Aditya", "Gowtham", "Hari")

    win = Tk()
    win.geometry(f"{SIZE}x{SIZE}")
    win.resizable(False, False)
    game = GUI(win, players)
    win.mainloop()

