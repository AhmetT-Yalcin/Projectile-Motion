from Module_DBConnection import * 


class DBProjectiles(DBConnection):
    # DBConnection is parent class of DBProjectiles 
    # DBProjectiles inherits properties and methods from DBConnection class
    # it also contains additional methods specific to projectile objects
     
    def __init__(self, user_name):
        # __init__ function is a predefined function for classes in python
        # this function will be executed automatically when we define an object from this class
        
        # projectile table is named as "SavedProjectiles"
        self.table = "SavedProjectiles"

        # projectile table's primary key column is ProjectileName
        self.key_column = "ProjectileName"

        # set user_name property from use_name parameter
        self.user_name = user_name

        # call parent init function 
        # 
        super().__init__(self.table, self.key_column)

    def create_table(self):
        """
        creates SavedProjectiles in table the database
        This table contains projectile definitions defined by user
        
        Table Name : SavedProjectiles
        Table Columns : 
        ProjectileName VARCHAR(100) NOT NULL: 
        --> max 100 char, should not be empty
        UserName VARCHAR(100) NOT NULL:  
        --> max 100 char, should not be empty
        InitialVelocity FLOAT NOT NULL CHECK (InitialVelocity>0):
        --> float, should be greater than zero
        x FLOAT NOT NULL DEFAULT(0):
        --> float, should not be empty, default 0
        y FLOAT NOT NULL DEFAULT(0):
        --> float, should not be empty, default 0 
        z FLOAT NOT NULL DEFAULT(0):
        --> float, should not be empty, default 0 
        PRIMARY KEY (ProjectileName, UserName):
        --> ProjectileName + UserName is the primary key of the table
        , FOREIGN KEY (UserName) REFERENCES ProjectileUsers(UserName)
        --> UserName is the foreign key in the ProjectileUsers table. 
            UserName value should be in the ProjectileUsers table
        """


        try:
            # execute SavedProjectiles create tables script in the database
            self.cursor.execute(f""" 
                    CREATE TABLE SavedProjectiles(
                    ProjectileName VARCHAR(100) NOT NULL,  
                    UserName VARCHAR(100) NOT NULL, 
                    InitialVelocity FLOAT NOT NULL CHECK (InitialVelocity>0),
                    x FLOAT NOT NULL DEFAULT(0),
                    y FLOAT NOT NULL DEFAULT(0),
                    z FLOAT NOT NULL DEFAULT(0)  
                    , PRIMARY KEY (ProjectileName, UserName) 
                    , FOREIGN KEY (UserName) REFERENCES ProjectileUsers(UserName)
                    )  """)
            self.conn.commit()
        except Exception as e:
            print(f"Cannot create table SavedProjectiles - Error: {e}")
            raise

    def insert_defaults(self):
        # add example projectiles in the table for user
        try:
            print("Username: ", self.user_name)
            projectiles = [
                ('PROJ1',self.user_name,2,3,4,5),
                ('PROJ2',self.user_name,3,4,5,6),
            ]
            
            # execute insert script 
            self.cursor.executemany(f""" INSERT INTO SavedProjectiles
                    VALUES (?,?,?,?,?,?)""", projectiles)
            
            # save in the database
            self.conn.commit()
        except Exception as e:
            print(f"Error: {e}")
            raise


    def insert_row(self, ProjectileName, InitialVelocity, x, y, z):


        try:
            # ProjectileName should be at least 2 chars
            if len(ProjectileName) < 1: 
                print("ProjectileName should be at least 1 char") 
            else : 
                # execute insert script
                self.cursor.execute(f""" INSERT INTO SavedProjectiles
                        VALUES ('{ProjectileName}','{self.user_name}',  {InitialVelocity}, {x}, {y}, {z} )
                     """)
                # save in the database
                self.conn.commit()
        except Exception as e:
            print(f"Cannot insert {ProjectileName} - Error: {e}")
            raise


    def update_row(self, ProjectileName, InitialVelocity, x, y, z):
        # updates projectile in the projectile table 
        # parameters are coming from the gui  
               
        try:
            # ProjectileName should be at least 2 chars
            if len(ProjectileName) < 1: 
                print("ProjectileName should be at least 1 char") 
            else : 
                 # execute update script
                self.cursor.execute(f""" UPDATE SavedProjectiles
                        SET InitialVelocity = {InitialVelocity}, x = {x}, y = {y}, z = {z} 
                        WHERE  ProjectileName = '{ProjectileName}' and UserName='{self.user_name}'
                """)
                # save in the database
                self.conn.commit()
        except Exception as e:
            print(f"Cannot update {ProjectileName} - Error: {e}")
            raise

    # Polymorphism
    # defined here again because we need user_name also
    def delete_row(self, value):
        # deletes a projectile from the projectile table 
        # parameters are coming from the gui  
                
        try:
            # execute delete script
            self.cursor.execute(f""" DELETE FROM SavedProjectiles
                        WHERE  {self.key_column} = '{value}' and UserName ='{self.user_name}' """)
             
             # save changes the database
            self.conn.commit()
        except Exception as e:
            print(f"Error: {e}")
            raise
    
    # Polymorphism
    # defined here again because we need user_name also
    def read_row(self, key_value): 
        # reads a projectile from the projectile table 
        # parameters are coming from the gui  
                
        try: 
            # execute select script 
            self.cursor.execute(f""" SELECT * FROM SavedProjectiles WHERE {self.key_column} = '{key_value}' and UserName='{self.user_name}' """)
            # return row in a cursor
            return self.cursor.fetchall()
        
        except Exception as e:
            print(f"Error: {e}")
            raise
    
    # Polymorphism
    # defined here again because we need user_name also
    def read_all(self): 
        # returns all projectiles from the projectile table 

        try: 
             # execute select script 
            query = f""" SELECT * FROM SavedProjectiles WHERE UserName='{self.user_name}'"""
            self.cursor.execute(query)
            # return rows in a cursor
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error: {e}")
            raise