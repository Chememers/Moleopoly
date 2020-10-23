import PySimpleGUI as sg

sg.theme('DarkGreen1')   

layout = [  [sg.Text('New Game', font=('Comic Sans MS', 20))],
            [sg.InputText(), sg.Button('Add Player')],
            [sg.Text('Players:', font=('Comic Sans MS', 20))],
            [sg.Listbox(values=[], size=(30, 6))],
            [sg.Button('Play!'), sg.Button('Cancel')] ]

window = sg.Window('Mole-O-Poly', layout, element_justification="c")

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break
    print('You entered ', values[0])

window.close()