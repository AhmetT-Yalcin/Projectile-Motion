from Module_Gui import * 

login_window = ctk.CTk()
# create login_gui object from LoginGui class
login_gui = LoginGui(login_window)

login_window.mainloop()
login_window.quit()
print(login_gui.password_check, login_gui.current_user, login_gui.user_is_admin)

# if password is not correct, kill the program
if not login_gui.password_check:
    sys.exit()

main_window = ctk.CTk()

# create main_gui object from MainGui class
main_gui = MainGui(main_window,login_gui.current_user, login_gui.user_is_admin)

main_window.mainloop()
main_window.quit()
