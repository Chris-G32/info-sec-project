import sqlite3 as sl


class PasswordDB:
    # Function to create the database and table
    def create_database():
        # Connect to SQLite database (or create it if it doesn't exist)
        conn = sl.connect('gruskaDB.db')

        # Create a cursor object to execute SQL queries
        cursor = conn.cursor()

        # SQL query to create the table
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS logins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT,
            website TEXT
        );
        '''
        # Execute the SQL query to create the table
        cursor.execute(create_table_query)

        create_table_query = '''CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT
        );'''
        cursor.execute(create_table_query)

        # Commit changes and close the connection
        conn.commit()
        conn.close()

    def set_master_key():
        conn = sl.connect('gruskaDB.db')
        cursor = conn.cursor()

        # SQL query to insert new credentials
        insert_query = '''
        INSERT INTO users (username, password)
        VALUES (?, ?);
        '''
        try:
        # Execute the SQL query with the provided values
            cursor.execute(insert_query, ('MASTER', 'MASTER_PASS'))
        except:
            pass
        # Commit changes and close the connection
        conn.commit()
        conn.close()
    # Function to insert new credentials into the table

    def insert_credentials(username:str, password:str, website:str):
        # Connect to the SQLite database
        conn = sl.connect('gruskaDB.db')
        cursor = conn.cursor()

        # SQL query to insert new credentials
        insert_query = '''
        INSERT INTO logins (username, password, website)
        VALUES (?, ?, ?);
        '''

        # Execute the SQL query with the provided values
        cursor.execute(insert_query, (username, password, website,))

        # Commit changes and close the connection
        conn.commit()
        conn.close()

    # Function to retrieve all credentials from the table
    def retrieve_credentials(password,isMaster):
        # Connect to the SQLite database
        conn = sl.connect('gruskaDB.db')
        cursor = conn.cursor()
        if isMaster:
            query = """
        SELECT username, password FROM logins 
        WHERE EXISTS (
            SELECT 1 FROM users 
            WHERE username = ? 
            AND password = ? 
        ); """
            cursor.execute(query,('MASTER',password))
        else:
            # SQL query to select all rows from the table
            query = '''
            SELECT * FROM logins;
            '''

        # Execute the SQL query
        cursor.execute(query)

        # Fetch all rows and return them
        credentials = cursor.fetchall()

        # Close the connection
        conn.close()

        return credentials


    def verify_master(master_key):
        conn = sl.connect('gruskaDB.db')
        cursor = conn.cursor()

        
        query="SELECT * FROM users WHERE username = 'MASTER' AND password= ?"

        cursor.execute(query, (master_key, ))
        # verify_query = 
        # cursor.execute("SELECT 1 FROM users \
        # WHERE username = 'MASTER' \
        # AND password = %s'",(master_key,))

        # Fetch all rows and return them
        credentials = cursor.fetchall()

        # Close the connection
        conn.close()
        return len(credentials)>0

# print(PasswordDB.verify_master("MASTER_PASS"))