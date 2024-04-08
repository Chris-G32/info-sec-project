import PySimpleGUI as sg
from passwords import PasswordUtils
from db import UserQueries,CredentialQueries
class View:
    def __init__(self) -> None:
        self.window=None
    def display(self,title):
        self.window=sg.Window(title,self.get_layout())
        res=self.run_event_loop()
        self.window.close()  
        return res
    def get_layout(self):
        raise NotImplementedError()
    def run_event_loop(self):
        raise NotImplementedError()
    
class InitialSigninView(View):
    def __init__(self):
        super()
    def display(self):
        return super().display("First Login")
    def get_layout(self):
        login_layout = [
        [sg.Text("Enter Password to Unlock"),sg.InputText(key="-PASS-INP-",enable_events=True),sg.Text("Weak", key="-STRENGTH-")],
        [sg.Button("Set Pass",bind_return_key=True, key="-SET-")]
        ]
        return login_layout
    def run_event_loop(self):
        while True:
            event, values = self.window.read()
            # if user closes window or clicks cancel
            if event == sg.WIN_CLOSED or event == 'Cancel':
                break
            elif event=="-SET-":
                if not self.try_set_user_pass(values):
                    sg.popup("Password is not strong enough!")
            elif event == "-PASS-INP-":
                self.on_password_update(values)
    def on_password_update(self,values):
        strength = PasswordUtils.score_password_strength(values['-PASS-INP-'])
        # Rate strength and give feedback
        if (PasswordUtils.is_excellent(strength)):
            self.window['-STRENGTH-'].update(value="Excellent")
        elif (PasswordUtils.is_strong(strength)):
            self.window['-STRENGTH-'].update(value="Strong")
        elif (PasswordUtils.is_ok(strength)):
            self.window['-STRENGTH-'].update(value="OK")
        else:
            self.window['-STRENGTH-'].update(value="Weak")
    #Returns true on success, false on fail
    def try_set_user_pass(self,values):
        pw=values['-PASS-INP-']
        strength = PasswordUtils.score_password_strength(pw)
        if PasswordUtils.is_strong(strength):
            UserQueries.create_local(pw)
            self.window.close()
            return True
        return False
        
class LoginView(View):
    def __init__(self):
        super()
    def display(self):
        return super().display("Login")
    def get_layout(self):
        login_layout = [
            [sg.Text("Enter Password to Unlock"), sg.Checkbox("master/local", key="-MASTER-FLAG-")],
            [sg.InputText(key="-USER-PASS-"), sg.Button("Unlock",bind_return_key=True, key="-REQ-UNLOCK-")]
        ]
        return login_layout
    def run_event_loop(self):
        authenticated_password=None
        authenticated_user=None
        # Event Loop to process "events" and get the "values" of the inputs
        while True:
            event, values = self.window.read()

            # if user closes window or clicks cancel
            if event == sg.WIN_CLOSED or event == 'Cancel':
                return (authenticated_user,authenticated_password)
            elif event == '-REQ-UNLOCK-':
                is_master=values['-MASTER-FLAG-']
                password=values['-USER-PASS-']
                user='MASTER' if is_master else 'LOCAL'
                if(UserQueries.password_correct(user,password)):
                    authenticated_password=password
                    authenticated_user=user
                    self.window.close()
class KeyChainView(View):
    def __init__(self,user,pw):
        super()
        self.user=user
        self.pw=pw
    def display(self):
        return super().display(f"{self.user}'s Keychain")
    def get_layout(self):
        headers = [[sg.Column([[sg.Text("Site")]], key='-SITES-'), sg.Column([[sg.Text("Username")]],
                                                                     key='-USERS-'), sg.Column([[sg.Text("Password")]], key='-PASSWORDS-')]]
        site_adder_layout = [[sg.Text("Site To Add: "), sg.Input(key='-SITE-INP-')],
                     [sg.Text("Username: "), sg.Input(key='-USER-INP-')],
                     [sg.Text("Password: "), sg.Input(
                         key='-PASS-INP-', enable_events=True), sg.Text("Weak", key="-STRENGTH-")],
                     [sg.Button("Generate Password", key="-GEN-"),sg.Button("Add Password", key="-ADD-PASS-")]]
        return [[sg.Column(headers, key='-BODY-')],
          [sg.Column(site_adder_layout, visible=False, key='-CREATE-CREDS-')]]
    def run_event_loop(self):
        self.window.finalize()
        for i in CredentialQueries.retrieve_credentials(self.user,self.pw):
            self.add_credentials_to_layout(i)
        if self.user=='LOCAL':
            self.window['-CREATE-CREDS-'].update(visible=True)

        while True:
            event, values = self.window.read()

            # if user closes window or clicks cancel
            if event == sg.WIN_CLOSED or event == 'Cancel':
                break
            elif event == "-PASS-INP-":
                self.on_password_update(values)
            elif event == "-ADD-PASS-":
                if PasswordUtils.is_excellent(PasswordUtils.score_password_strength(values['-PASS-INP-'])):
                    self.save_credentials(values)
                else:
                    sg.popup("Password is not strong enough!")
            # password generator functionality
            elif event == '-GEN-':
                password=PasswordUtils.generate_password()
                self.window['-PASS-INP-'].update(value=password)
                self.window.write_event_value('-PASS-INP-', password)#Raise event for password input update

    def save_credentials(self,values):
        CredentialQueries.insert_credentials(values['-SITE-INP-'], values['-USER-INP-'], values['-PASS-INP-'],self.pw)
        self.add_credentials_to_layout([values['-SITE-INP-'], values['-USER-INP-'], values['-PASS-INP-']])

    def add_credentials_to_layout(self,credentials):
        self.window.extend_layout(self.window['-SITES-'], [[sg.Text(credentials[0])]])
        self.window.extend_layout(self.window['-USERS-'], [[sg.Text(credentials[1])]])
        password = ''
        if (len(credentials) > 2):
            password = credentials[2]
        self.window.extend_layout(self.window['-PASSWORDS-'], [[sg.Text(password)]])

    def on_password_update(self,values):
        strength = PasswordUtils.score_password_strength(values['-PASS-INP-'])
        # Rate strength and give feedback
        if (PasswordUtils.is_excellent(strength)):
            self.window['-STRENGTH-'].update(value="Excellent")
        elif (PasswordUtils.is_strong(strength)):
            self.window['-STRENGTH-'].update(value="Strong")
        elif (PasswordUtils.is_ok(strength)):
            self.window['-STRENGTH-'].update(value="OK")
        else:
            self.window['-STRENGTH-'].update(value="Weak")