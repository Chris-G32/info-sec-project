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
site_adder_layout=[[sg.Text("Site To Add: "),sg.Input(key='-SITE-INP-')],
            [sg.Text("Username: "),sg.Input(key='-USER-INP-')],
            [sg.Text("Password: "),sg.Input(key='-PASS-INP-',enable_events=True),sg.Text("Weak",key="-STRENGTH-")],
            [sg.Button("Add Password",disabled=True,key="-ADD-PASS-")]]
# All the stuff inside your window.
layout = [  [sg.Text("Enter Password to Unlock"),sg.Checkbox("master/local",key="-MASTER-FLAG-")],
            [sg.InputText(key="-USER-PASS-"),sg.Button("Unlock",bind_return_key=True,key="-REQ-UNLOCK-")],
            [sg.Column(headers,visible=False,key='-BODY-')],
            [sg.Column(site_adder_layout,visible=False,key='-CREATE-CREDS-')]
        ]

# Create the Window
window = sg.Window('Hello Example', layout)
authenticated=False
def unlockGUI(master=False):
    authenticated=True
    window['-BODY-'].update(visible=True)
    if master:
        window["-REQ-UNLOCK-"].update(disabled=True)
    else:
        window['-CREATE-CREDS-'].update(visible=True)
        window['-ADD-PASS-'].update(disabled=False)
    # window['-USER-INP-'].update(visible=True)
    # window['-PASS-INP-'].update(visible=True)
    # window['-SITE-INP-'].update(visible=True)
    
    # window['-ADD-PASS-'].update(visible=True)
    # window['-ADD-PASS-'].update(visible=True)
    # window['-ADD-PASS-'].update(visible=True)

def add_credentials_to_layout(credentials):
    window.extend_layout(window['-SITES-'],[[sg.Text(credentials[0])]])
    window.extend_layout(window['-USERS-'],[[sg.Text(credentials[1])]])
    password=''
    if(len(credentials)>2):
        password=credentials[2]
    window.extend_layout(window['-PASSWORDS-'],[[sg.Text(password)]])

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()

    # if user closes window or clicks cancel
    if event == sg.WIN_CLOSED or event == 'Cancel':
        break
    elif event=='-REQ-UNLOCK-':
        credentials=[]
        if(values['-MASTER-FLAG-']):
            #sg.popup(str(PasswordDB.verify_master(values['-USER-PASS-'])))
           credentials=PasswordDB.retrieve_credentials(values['-USER-PASS-'],True)
           unlockGUI(True)
        elif matchesPassword(values['-USER-PASS-']):
            credentials=PasswordDB.retrieve_credentials(values['-USER-PASS-'],False)
            unlockGUI()
        for i in credentials:
               add_credentials_to_layout(i)
        
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
            PasswordDB.insert_credentials(values['-SITE-INP-'],values['-USER-INP-'],values['-PASS-INP-'])
            add_credentials_to_layout([values['-SITE-INP-'],values['-USER-INP-'],values['-PASS-INP-']])
        else:
            sg.popup("Password is not strong enough!")
    #password generator functionality
    elif event=='-GENERATE-':
        pass
        # print('Hello', values[0], '!')

window.close()
