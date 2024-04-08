import sqlite3 as sl
from passwords import PasswordUtils

class UserQueries:
    def create_user(username,password):
        conn = sl.connect('gruskaDB.db')
        cursor = conn.cursor()

        # SQL query to insert new credentials
        insert_query = '''
        INSERT INTO users (username, password)
        VALUES (?, ?);
        '''
        passwordHash=None
        try:
            #Hash password
            passwordHash=PasswordUtils.hash_password(password)
        except:
            raise RuntimeError("Password hash failed!")
        
        try:
            # Execute the SQL query with the provided values
            cursor.execute(insert_query, (username, passwordHash,))
        except:
            return False
        
        # Commit changes and close the connection
        conn.commit()
        conn.close()
        return True
    
    def create_master_if_not_exists():
        return UserQueries.create_user("MASTER","admin")
    def create_local(password):
        return UserQueries.create_user("LOCAL",password)
    def user_exists(username:str):
        conn = sl.connect('gruskaDB.db')
        cursor = conn.cursor()
        
        query="SELECT * FROM users WHERE username = ?"

        cursor.execute(query, (username, ))

        # Fetch all rows and return them
        credentials = cursor.fetchall()

        # Close the connection
        conn.close()
        return len(credentials)>0
    #true on success
    def password_correct(user,password):
        conn = sl.connect('gruskaDB.db')
        cursor = conn.cursor()
        
        query="SELECT * FROM users WHERE username = ? AND password= ?"

        cursor.execute(query, (user,PasswordUtils.hash_password(password), ))
        # verify_query = 
        # cursor.execute("SELECT 1 FROM users \
        # WHERE username = 'MASTER' \
        # AND password = %s'",(master_key,))

        # Fetch all rows and return them
        credentials = cursor.fetchall()

        # Close the connection
        conn.close()
        return len(credentials)>0

class CredentialQueries:
    def insert_credentials(website:str,username:str, password:str,user_pass:str):
        # Connect to the SQLite database
        conn = sl.connect('gruskaDB.db')
        cursor = conn.cursor()

        # SQL query to insert new credentials
        insert_query = '''
        INSERT INTO logins (website,username, password, iv)
        VALUES (?, ?, ?, ?);
        '''
        cipher_text,iv=PasswordUtils.encrypt(user_pass,password)
        # Execute the SQL query with the provided values
        cursor.execute(insert_query, (website,username,cipher_text,iv,))

        # Commit changes and close the connection
        conn.commit()
        conn.close()

    # Function to retrieve all credentials from the table
    def retrieve_credentials(user:str,password:str):
        # Connect to the SQLite database
        conn = sl.connect('gruskaDB.db')
        cursor = conn.cursor()
        passwordHash=None
        try:
            #Hash password
            passwordHash=PasswordUtils.hash_password(password)
        except:
            raise RuntimeError("Password hash failed!")
        
        if user=='MASTER':
            query = """
        SELECT website,username FROM logins 
        WHERE EXISTS (
            SELECT 1 FROM users 
            WHERE username = ? 
            AND password = ? 
        ); """
            cursor.execute(query,('MASTER',passwordHash,))
        else:
            # SQL query to select all rows from the table
            query = """
        SELECT website,username,password,iv FROM logins 
        WHERE EXISTS (
            SELECT 1 FROM users 
            WHERE username = ?
            AND password = ? 
        ); """

            # Execute the SQL query
            cursor.execute(query,('LOCAL',passwordHash,))

        # Fetch all rows and return them
        credentials = cursor.fetchall()
        decrypted_credentials=[]
        if( user!='MASTER'):
            #Decrypt passwords
            for cred in credentials:
                print("encrypted")
                print(cred[2])
                plaintext_pass=PasswordUtils.decrypt(password,cred[2],cred[3])
                decrypted_credentials.append([cred[0],cred[1],plaintext_pass])
                
            
        # Close the connection
        conn.close()

        return decrypted_credentials

class PasswordDB:
    HASH_SIZE=32
    # Function to create the database and table
    def create_database_if_not_exists():
        # Connect to SQLite database (or create it if it doesn't exist)
        conn = sl.connect('gruskaDB.db')

        # Create a cursor object to execute SQL queries
        cursor = conn.cursor()

        # SQL query to create the table
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS logins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            website TEXT,
            username TEXT,
            password BLOB,
            iv BLOB
        );
        '''
        # Execute the SQL query to create the table
        cursor.execute(create_table_query)
        
        # Create users table
        create_table_query = f'''CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password BLOB
        );'''
        cursor.execute(create_table_query)

        # Commit changes and close the connection
        conn.commit()
        conn.close()
