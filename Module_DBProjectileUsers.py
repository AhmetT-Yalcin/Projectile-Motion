from Module_DBConnection import * 
import hashlib

class DBProjectileUsers(DBConnection): 
    def __init__(self):
        # __init__ function is a predefined function for classes in python
        # this function will be executed automatically when we define an object from this class
                
        self.table = "ProjectileUsers"
        self.key_column = "UserName"
        super().__init__(self.table, self.key_column)

    def create_table(self):
        """
        creates SavedProjectiles in table the database
        This table contains projectile definitions defined by user
        
        Table Name:ProjectileUsers 
        Table Columns :         
        UserName VARCHAR(100) NOT NULL PRIMARY KEY
        --> max 100 char, should not be empty
        Password VARCHAR(100) NOT NULL CHECK( LENGTH(Password)>5 ),
        --> max 100 char, should not be more than 5 chars
        isAdmin CHAR(1) NOT NULL DEFAULT('N')
        --> 1 char, should not be empty, default N (not admin)
        --> 
        """
        try:
            # execute SavedProjectiles create tables script in the database
            self.cursor.execute(f""" CREATE TABLE ProjectileUsers(
                    UserName VARCHAR(100) NOT NULL PRIMARY KEY,
                    Password VARCHAR(100) NOT NULL CHECK( LENGTH(Password)>5 ),
                    isAdmin CHAR(1) NOT NULL DEFAULT('N')
                    ) """)
            # save changes in the database
            self.conn.commit()
        except Exception as e:
            print(f"Cannot create table ProjectileUsers - Error: {e}")
            raise

    def insert_defaults(self):
        # add default users in the ProjectileUsers table 

        try:

            users = [
                # user : admin, password: admin with hashed value, isAdmin = Y
                ('admin', hashlib.sha1("admin".encode()).hexdigest(),"Y" ),
                # user : ahmet, password: ahmet with hashed value, isAdmin = N
                ('ahmet',hashlib.sha1("ahmet".encode()).hexdigest(), "N" ),
            ]
            
            # execute insert script 
            self.cursor.executemany(f""" INSERT INTO ProjectileUsers
                    VALUES (?,?,?)""", users)
            # save changes
            self.conn.commit()
        except Exception as e:
            print(f"Error: {e}")
            raise


    def insert_row(self, UserName, password, admin):
        # insert user in the ProjectileUsers table 
        # parameters are coming from the gui 
        try:
            # username should be at least 1 char
            if len(UserName) < 1: 
                print("UserName should be at least 1 char") 
            else : 
                # execute insert script 
                self.cursor.execute(f""" INSERT INTO ProjectileUsers
                        VALUES ('{UserName}', '{hashlib.sha1(password.encode()).hexdigest()      }', '{admin}' )
                     """)
                # save changes
                self.conn.commit()
        except Exception as e:
            print(f"Cannot insert {UserName} - Error: {e}")
            raise


    def update_row(self, UserName, Password, admin):
        # update user in the ProjectileUsers table 
        # parameters are coming from the gui         
        try:
            # username should be at least 1 char
            if len(UserName) < 1: 
                print("ProjectileName should be at least 1 char") 
            else : 
                # execute update script 
                self.cursor.execute(f""" UPDATE ProjectileUsers
                        SET Password = '{hashlib.sha1(Password.encode()).hexdigest()      }' , 
                        isAdmin = '{admin}'
                        WHERE  UserName = '{UserName}'
                """)
                # save changes
                self.conn.commit()
        except Exception as e:
            print(f"Cannot update {UserName} - Error: {e}")
            raise

    def update_password(self, UserName, Password):
        # update password in the ProjectileUsers table 
        # parameters are coming from the gui         

        try:
            # username should be at least 1 char
            if len(UserName) < 1: 
                print("ProjectileName should be at least 1 char") 
            else : 
                # execute update script 
                self.cursor.execute(f""" UPDATE ProjectileUsers
                        SET Password = '{hashlib.sha1(Password.encode()).hexdigest()      }' 
                        WHERE  UserName = '{UserName}'
                """)
                # save changes
                self.conn.commit()
        except Exception as e:
            print(f"Cannot update {UserName} - Error: {e}")
            raise