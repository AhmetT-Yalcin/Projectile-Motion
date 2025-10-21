import sqlite3
import os

# this is the parent class to connect database and main functions 
class DBConnection(): 
    
    def __init__(self, table_name, key_column):
        # __init__ function is a predefined function for classes in python
        # this function will be executed automatically when we define an object from this class

        # connects to database 
        # get current working directory
        cwd = os.getcwd()
        print("Current Folder:", cwd)

        # open sqllite database which is in the current directory named projectile.db
        self.conn = sqlite3.connect(cwd+'/projectile.db')
        
        # execute sqllite function to enable foreign key usage
        self.conn.execute("PRAGMA foreign_keys = 1") # Turn ON foreign key constraints
        
        # open cursor in the database - We will execute database operations like select, insert, update, delete with this cursor
        self.cursor = self.conn.cursor()

        # define table name and primary key fields
        self.table = table_name
        self.key_column = key_column

    
    def drop_table(self):
        # drop a table from database
        # table name is the property of the object

        try:
            # execute drop table command in the database
            self.cursor.execute(f""" DROP TABLE {self.table} """)
            # save changes in the database
            self.conn.commit()
        except Exception as e:
            print(f"Error: {e}")
            # raise the error to the caller if exists
            raise

    def delete_row(self, value):
        # deletes a row from the table
        # table name is the property of the object

        try:
            # delete a row from the table
            self.cursor.execute(f""" DELETE FROM {self.table}
                        WHERE  {self.key_column} = '{value}'""")
            
            # save changes in the database
            self.conn.commit()
        except Exception as e:
            print(f"Error: {e}")
            # raise the error to the caller if exists
            raise

    def read_all(self): 
        # reads all rows from the table
        # table name is the property of the object

        try: 
            # select all rows in a cursor
            self.cursor.execute(f""" SELECT * FROM {self.table} """)
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error: {e}")
            # raise the error to the caller if exists
            raise

    def read_row(self, key_value): 
        # reads a row from the table
        # table name is the property of the object        

        try: 
            # select a row in a cursor - filter the row by key_value parameter
            self.cursor.execute(f""" SELECT * FROM {self.table} WHERE {self.key_column} = '{key_value}'""")
            return self.cursor.fetchone()
        except Exception as e:
            print(f"Error: {e}")
            raise


    def __del__(self):
        # __del__ function is a predefined function for classes in python
        # this function will be executed automatically when the object terminated

        try: 
            # close the connection
            self.conn.close()
        except Exception as e:
            print(f"Error: {e}")
            raise
