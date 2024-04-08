from db import PasswordDB,UserQueries
from view import InitialSigninView,LoginView,KeyChainView

#Class modeling simple app window flow
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
        while(pw!=None):
            #Normal app view
            if KeyChainView(user,pw).display()=='LOGOUT':
                user,pw=LoginView().display()
            else:
                break
