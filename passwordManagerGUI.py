import PySimpleGUI as sg
from db import PasswordDB
import passwords as pw
def getPasswordList():
    password_headers= []

    return password_headers
def matchesPassword(inp:str):
    return inp=="PASS"

PasswordDB.create_database()
PasswordDB.set_master_key()
headers=[[sg.Column([[sg.Text("Site")]],key='-SITES-'),sg.Column([[sg.Text("Username")]],key='-USERS-'),sg.Column([[sg.Text("Password")]],key='-PASSWORDS-')]]

# All the stuff inside your window.
layout = [  [sg.Text("Enter Password to Unlock"),sg.Checkbox("master/local",key="-MASTER-FLAG-")],
            [sg.InputText(key="-USER-PASS-"),sg.Button("Unlock",bind_return_key=True,key="-REQ-UNLOCK-")],
            [sg.Column(headers,visible=False,key='-BODY-')],
            [sg.Text("Site To Add: "),sg.Input(key='-SITE-INP-')],
            [sg.Text("Username: "),sg.Input(key='-USER-INP-')],
            [sg.Text("Password: "),sg.Input(key='-PASS-INP-',enable_events=True),sg.Text("Weak",key="-STRENGTH-")],
            [sg.Button("Add Password",disabled=True,key="-ADD-PASS-")]
        ]

# Create the Window
window = sg.Window('Hello Example', layout)
authenticated=False
def unlockGUI():
    authenticated=True
    window['-BODY-'].update(visible=True)
    
    # window['-USER-INP-'].update(visible=True)
    # window['-PASS-INP-'].update(visible=True)
    # window['-SITE-INP-'].update(visible=True)
    window['-ADD-PASS-'].update(disabled=False)
    # window['-ADD-PASS-'].update(visible=True)
    # window['-ADD-PASS-'].update(visible=True)
    # window['-ADD-PASS-'].update(visible=True)

def populate_passwords():
    window.extend_layout(window['-SITES-'],[[sg.Text("testSITE")]])
    window.extend_layout(window['-USERS-'],[[sg.Text("testUSER")]])
    window.extend_layout(window['-PASSWORDS-'],[[sg.Text("testPASS")]])
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()

    # if user closes window or clicks cancel
    if event == sg.WIN_CLOSED or event == 'Cancel':
        break
    elif event=='-REQ-UNLOCK-':
        if(values['-MASTER-FLAG-']):
           sg.popup(str(PasswordDB.verify_master(values['-USER-PASS-'])))
        if matchesPassword(values['-USER-PASS-']):
            
            unlockGUI()
            populate_passwords()
            # window.extend_layout(window['-BODY-'],getPasswordList())
    elif event=="-PASS-INP-":
        WEAK=20
        STRONG=26
        EXCELLENT=32
        strength=pw.evaluateStrength(values['-PASS-INP-'])
        #Rate strength and give feedback
        if(strength>EXCELLENT):
            window['-STRENGTH-'].update(value="Excellent")
        elif(strength>STRONG):
            window['-STRENGTH-'].update(value="Strong")
        elif (strength>WEAK):
            window['-STRENGTH-'].update(value="OK")
        else:
            window['-STRENGTH-'].update(value="Weak")
    elif event=="-ADD-PASS-":
        if pw.evaluateStrength(values['-PASS-INP-'])>WEAK:
            pass
        else:
            sg.popup("Password is not strong enough!")
        # print('Hello', values[0], '!')

window.close()
