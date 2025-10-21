from Module_DBProjectiles import * 
from Module_DBProjectileUsers import * 

import tkinter as tk
import customtkinter as ctk


def admin_create_user(root):
    """
    creates admin user screen
    """
    def create_user():
        """
        insert a new user row in the database
        """
        try:
            # create users object from DBProjectileUsers class
            users = DBProjectileUsers()
            print("user:", cu_entry_user_var.get(), " password:",cu_entry_password_var.get(), 'xx' ,cu_check_admin_var.get(),'yy' )
            # set admin variable if user selected as admin 
            admin = "Y" if cu_check_admin_var.get() == "on" else "N"
            
            # insert a new user into the database using Users object
            users.insert_row(cu_entry_user_var.get(), cu_entry_password_var.get(),admin)
            print("User Created")
            tk.messagebox.showinfo("Info","User Created") 
            
        except Exception as e:
            # show message if there is an error
            tk.messagebox.showinfo("Error",f"Cannot create user - Error: {e}") 
            print(f"Cannot create user - Error: {e}") 


    create_user_window = ctk.CTkToplevel(root)
    create_user_window.title("Create User")
    create_user_window.geometry("300x250")
    
    create_user_window.columnconfigure(0, weight=1)
    create_user_window.rowconfigure(0, weight=1)

    #entry_user_var=ctk.StringVar()
    cu_entry_user_var=ctk.StringVar()
    cu_entry_password_var=ctk.StringVar()
    

    cu_label_user = ctk.CTkLabel(create_user_window, text="User:").grid(row=0, column=0 )
    cu_entry_user = ctk.CTkEntry(create_user_window,textvariable = cu_entry_user_var, font=('calibre',15,'normal')).grid(row=0, column=1)

    cu_label_password = ctk.CTkLabel(create_user_window, text="Password:").grid(row=1, column=0)
    cu_entry_password = ctk.CTkEntry(create_user_window,textvariable = cu_entry_password_var, font=('calibre',15,'normal')).grid(row=1, column=1)

    cu_check_admin_var = ctk.StringVar()
    cu_label_admin = ctk.CTkLabel(create_user_window, text="Admin:").grid(row=2, column=0)
    cu_checkbox_admin = ctk.CTkCheckBox(master=create_user_window, text="", variable=cu_check_admin_var, onvalue="on", offvalue="off").grid(row=2, column=1)
    

    create_password_button = ctk.CTkButton(create_user_window, text="Create User", command=create_user)
    create_password_button.grid(row=4, columnspan=2, pady=20)
    create_user_window.attributes("-topmost","true")
    create_user_window.mainloop()
    create_user_window.quit()

def admin_reset_password(root):
    """
    creates admin user reset screen
    """
    def change_password():
        # print(user_combobox.get(), entry_password_var2.get())
        users.update_password(user_combobox.get(), rp_entry_password_var.get())
        print("password Changed")
        tk.messagebox.showinfo("Info","Password Changed") 

    rp_window = ctk.CTkToplevel(root)
    rp_window.title("Reset Password")
    rp_window.geometry("230x150")
    
    rp_window.columnconfigure(0, weight=1)
    rp_window.rowconfigure(0, weight=1)

    #entry_user_var=ctk.StringVar()
    rp_entry_password_var=ctk.StringVar()

    rp_label_user = ctk.CTkLabel(rp_window, text="User:").grid(row=0, column=0, padx=5, pady=5)

    rp_user_combobox_var = ctk.StringVar(value="option 444")  # set initial value

    # create Users object from DBProjectileUsers class
    users = DBProjectileUsers()
    # read all users from database
    db_rows = users.read_all()

    # add users into user_list
    user_list=[]
    for row in db_rows:
        user_list.append(row[0])
        

        
    # fill user_combobox with user_list
    user_combobox = ctk.CTkComboBox(master = rp_window, values=user_list)
    user_combobox.grid(row=0, column=1)

    label_password = ctk.CTkLabel(rp_window, text="Password:").grid(row=1, column=0, padx=5, pady=5)
    entry_password = ctk.CTkEntry(rp_window,show="*",textvariable = rp_entry_password_var, font=('calibre',15,'normal')).grid(row=1, column=1,padx=5, pady=5)


    change_password_button = ctk.CTkButton(rp_window, text="Change Password", command=change_password)
    change_password_button.grid(row=4, columnspan=2, pady=20)
    rp_window.attributes("-topmost","true")
    rp_window.mainloop()
    rp_window.quit()



def admin_delete_user(root):
    """
    creates admin delete user screen
    """
    def delete_user():
        # deletes a user from database
        users.delete_row(user_combobox.get())
        print("user deleted")
        tk.messagebox.showinfo("Info","user deleted") 

    du_window = ctk.CTkToplevel(root)
    du_window.title("Delete User")
    du_window.geometry("230x150")
    
    du_window.columnconfigure(0, weight=1)
    du_window.rowconfigure(0, weight=1)

    #entry_user_var=ctk.StringVar()
    du_entry_password_var=ctk.StringVar()

    du_label_user = ctk.CTkLabel(du_window, text="User:").grid(row=0, column=0, padx=5, pady=5)

    du_user_combobox_var = ctk.StringVar(value="option 444")  # set initial value

    # create Users object from DBProjectileUsers class
    users = DBProjectileUsers()
    # add users into user_list
    db_rows = users.read_all()
    # add users into user_list
    user_list=[]
    for row in db_rows:
        user_list.append(row[0])
        
    user_combobox = ctk.CTkComboBox(master = du_window, values=user_list)
    user_combobox.grid(row=0, column=1)


    delete_user_button = ctk.CTkButton(du_window, text="Delete User", command=delete_user)
    delete_user_button.grid(row=4, columnspan=2, pady=20)
    du_window.attributes("-topmost","true")
    du_window.mainloop()
    du_window.quit()


def change_my_password(root, current_user):
    """
    creates password change screen
    """
    def change_password():
        # changes password in the database 

        if password_db == hashlib.sha1(entry_old_password_var.get().encode()).hexdigest():
            # call update_password of user object
            users.update_password(current_user , entry_new_password_var.get())
            tk.messagebox.showinfo("Info","Password Changed") 
        else:
            tk.messagebox.showinfo("Error","Old password is not correct") 
            print("password not Changed")

    cmp_window = ctk.CTkToplevel(root)
    cmp_window.title("Change My Password")
    cmp_window.geometry("250x150")
    
    cmp_window.columnconfigure(0, weight=1)
    cmp_window.rowconfigure(0, weight=1)
    
    entry_old_password_var=ctk.StringVar()
    entry_new_password_var=ctk.StringVar()

    # create Users object from DBProjectileUsers class
    users = DBProjectileUsers()
    #user=entry_user_var.get()
    #password = entry_password_var.get()
    #print(user, password)
    
    # read user information from database
    db_row = users.read_row(current_user)
    # password is second object in the row 
    password_db = db_row[1]


    cmp_label_old_password = ctk.CTkLabel(cmp_window, text="Old Password:").grid(row=1, column=0, padx=5, pady=5)
    cmp_entry_old_password = ctk.CTkEntry(cmp_window,show="*",textvariable = entry_old_password_var, font=('calibre',15,'normal')).grid(row=1, column=1,padx=5, pady=5)

    cmp_label_new_password = ctk.CTkLabel(cmp_window, text="New Password:").grid(row=2, column=0, padx=5, pady=5)
    cmp_entry_new_password = ctk.CTkEntry(cmp_window,show="*",textvariable = entry_new_password_var, font=('calibre',15,'normal')).grid(row=2, column=1,padx=5, pady=5)



    change_password_button = ctk.CTkButton(cmp_window, text="Change Password", command=change_password)
    change_password_button.grid(row=4, columnspan=2, pady=20)
    cmp_window.attributes("-topmost","true")
    cmp_window.mainloop()
    cmp_window.quit()


# -----------------------------
