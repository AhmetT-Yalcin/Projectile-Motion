password_ok = False
from Module_DBProjectiles import * 
from Module_DBProjectileUsers import * 

"""
Users = DBProjectileUsers()
Users.drop_table()
Users.create_table()
Users.insert_defaults()
"""
projectiles = DBProjectiles("ahmet")
# projectiles.drop_table()
projectiles.create_table()
projectiles.insert_defaults()



