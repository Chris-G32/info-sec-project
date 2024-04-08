from db import PasswordDB,UserQueries
from view import InitialSigninView,LoginView,KeyChainView

class App:
    #Start up apps backend
    def __init__(self):
        PasswordDB.create_database_if_not_exists()
        UserQueries.create_master_if_not_exists()
        
    def start(self):
        #Display password set screen if necessary
        if not UserQueries.user_exists("LOCAL"):
            InitialSigninView().display()
        user,pw=LoginView().display()

        #Normal app view
        KeyChainView(user,pw).display()
        
        
app=App()
app.start()
#myPass123!