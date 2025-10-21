import tkinter as tk
import customtkinter as ctk
from Module_DBProjectiles import * 
from Module_DBProjectileUsers import * 
from Module_UserOperations import *
from Module_CalculationFunctions import *
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import matplotlib.figure
import sys
import math

# Login Gui Class
class LoginGui:
    def __init__(self, login_window):

        self.login_window = login_window
        self.password_check = False
        self.user_is_admin = False
        self.current_user = ""
        self.login_window.title("LOGIN")
        ctk.set_appearance_mode("light")
        self.login_window.geometry("230x150")

        self.login_window.columnconfigure(0, weight=1)
        self.login_window.rowconfigure(0, weight=1)

        login_frame = ctk.CTkFrame(self.login_window)
        login_frame.grid()

        self.entry_username=ctk.StringVar()
        self.entry_password=ctk.StringVar()

        label_user = ctk.CTkLabel(login_frame, text="User:").grid(row=0, column=0, padx=5, pady=5)
        entry_user = ctk.CTkEntry(login_frame,textvariable = self.entry_username, font=('calibre',15,'normal')).grid(row=0, column=1,padx=5, pady=5)

        label_password = ctk.CTkLabel(login_frame, text="Password:").grid(row=1, column=0, padx=5, pady=5)
        entry_password = ctk.CTkEntry(login_frame,show="*",textvariable = self.entry_password, font=('calibre',15,'normal')).grid(row=1, column=1,padx=5, pady=5)

        sign_in_button = ctk.CTkButton(login_frame, text="Check Password", command=self.check_password)
        sign_in_button.grid(row=4, columnspan=2, pady=20)


    def check_password(self):
        """
        check password from database
        """
        self.password =self.entry_password.get()
        self.current_user=self.entry_username.get()
        print("check_password 1 : ", self.current_user,self.password)

        # create users object from DBProjectileUsers
        Users = DBProjectileUsers()

        # read user information from database
        db_row =   Users.read_row(self.current_user)
        
        if db_row: 
            # user exists in the database
            # admin check 
            if db_row[2] =="Y":
                self.user_is_admin = True
            print("UserIsAdmin : ", self.user_is_admin)
            
            # password check - password is same as database
            if db_row[1] == hashlib.sha1(self.password.encode()).hexdigest():
                print("password is correct")
                del Users
                self.password_check = True
                self.login_window.destroy()
            else:
                print("password is wrong")
                self.password_check=False
                tk.messagebox.showinfo("Error","Wrong password") 
        else:
            # user does not exist in the database
            password_db = None
            tk.messagebox.showinfo("Error","User does not exist") 

        #print("check_password 2:", self.CurrentUser, self.UserIsAdmin, self.password_check)


# creates main Gui
class MainGui:
    
    def __init__(self, main_window, current_user, user_is_admin):

        self.main_window = main_window
        self.current_user= current_user
        self.user_is_admin= user_is_admin

        self.gravity = 9.81
        self.graph_fastest_angle = 0
        self.graph_fastest_time = 0

        self.main_window.title("Bullet Trajectory Calculator")
        ctk.set_appearance_mode("light")
        self.main_window.geometry("1280x720")

        self.main_window.columnconfigure(0, weight=1)
        self.main_window.columnconfigure(1, weight=1)
        self.main_window.rowconfigure(0, weight=1)

        # create projectiles object from DBProjectiles class
        self.projectiles = DBProjectiles(self.current_user)
        self.add_menu_widget()
        self.add_projectile_widgets()
        self.add_graph_frame()

    def add_menu_widget(self):
        menubar = tk.Menu(self.main_window)
        file_menu = tk.Menu(menubar, tearoff=0)

        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.main_window.quit)

        menubar.add_cascade(label="File", menu=file_menu)

        user_menu = tk.Menu(menubar, tearoff=0)
        user_menu.add_command(label="Change My Password", command=lambda : change_my_password(self.main_window, self.current_user))
        if self.user_is_admin: 
            user_menu.add_separator()
            user_menu.add_command(label="Reset Password", command=lambda : admin_reset_password(self.main_window))
            user_menu.add_command(label="Create User", command=lambda : admin_create_user(self.main_window))
            user_menu.add_command(label="Delete User", command=lambda : admin_delete_user(self.main_window))

        menubar.add_cascade(label="User Operations", menu=user_menu)

        self.main_window.config(menu=menubar)    


    def add_projectile_widgets(self):
        # Frames
        main_frame = ctk.CTkFrame(self.main_window)
        main_frame.grid(row=0, column=0)

        entry_frame = ctk.CTkFrame(main_frame) 
        entry_frame.grid(row=0, column=0, pady=20, padx=20) 

        result_frame = ctk.CTkFrame(main_frame) 
        result_frame.grid(row=1, column=0, pady=20, padx=20) 

        # Create input boxes
        self.entry_projectile_name = ctk.CTkEntry(entry_frame)
        self.entry_speed = ctk.CTkEntry(entry_frame)
        self.entry_vector_x = ctk.CTkEntry(entry_frame)
        self.entry_vector_y = ctk.CTkEntry(entry_frame)
        self.entry_vector_z = ctk.CTkEntry(entry_frame)

        # Create labels for input boxes
        label_projectile_name = ctk.CTkLabel(entry_frame, text="Projectile name: ")
        label_speed = ctk.CTkLabel(entry_frame, text="Initial bullet speed (m/s): ")
        label_vector_x = ctk.CTkLabel(entry_frame, text="x (m): ")
        label_vector_y = ctk.CTkLabel(entry_frame, text="y (m): ")
        label_vector_z = ctk.CTkLabel(entry_frame, text="z (z): ")


        
        projectile_list = self.projectiles.read_all()
        projectile_name_list  = [x[0] for x in projectile_list]
        print("projectile_name_list: ", projectile_name_list)


        # Projectile buttons
        calculate_button = ctk.CTkButton(entry_frame, text="Calculate", command=self.projectile_calculate)
        print("graph_fastest_angle:", self.graph_fastest_angle, " graph_fastest_time:",self.graph_fastest_time)
        save_button = ctk.CTkButton(entry_frame, text="Save", command=self.projectile_save)
        delete_button = ctk.CTkButton(entry_frame, text="Delete", command=self.projectile_delete)

        self.combobox = ctk.CTkComboBox(entry_frame, values=projectile_name_list, command=self.projectile_combobox_refresh)


        # Graph trajectory
        #plot_button = tk.Button(root, text="Graph it!", command=())

        # Create labels to display results
        self.magnitude_label = ctk.CTkLabel(result_frame, text="Magnitude:")
        self.direction_label = ctk.CTkLabel(result_frame, text="Rotate (left/right): ")

        self.angle1_label = ctk.CTkLabel(result_frame, text="Angle 1: ")
        self.angle1_time_label = ctk.CTkLabel(result_frame, text="Time 1: ")

        self.angle2_label = ctk.CTkLabel(result_frame, text="Angle 2: ")
        self.angle2_time_label = ctk.CTkLabel(result_frame, text="Time 2: ")

        self.fastest_angle_label = ctk.CTkLabel(result_frame, text="Recommended angle: ")
        self.fastest_time_label = ctk.CTkLabel(result_frame, text="Recommended time: ")

        # Grid layout for labels and input boxes
        label_projectile_name.grid(row=0, column=0)
        self.entry_projectile_name.grid(row=0, column=1)

        label_speed.grid(row=1, column=0)
        self.entry_speed.grid(row=1, column=1)

        label_vector_x.grid(row=2, column=0)
        self.entry_vector_x.grid(row=2, column=1)

        label_vector_y.grid(row=3, column=0)
        self.entry_vector_y.grid(row=3, column=1)

        label_vector_z.grid(row=4, column=0)
        self.entry_vector_z.grid(row=4, column=1)

        # Position submit button
        calculate_button.grid(row=5, column=0)
        save_button.grid(row=5, column=1)
        delete_button.grid(row=5, column=2)

        self.combobox.grid(row=0, column=2)

        # Position labels for results
        self.magnitude_label.grid(row=0, column=0, sticky="W")
        self.direction_label.grid(row=1, column=0, sticky="W")

        self.angle1_label.grid(row=2, column=0, sticky="W")
        self.angle1_time_label.grid(row=3, column=0, sticky="W")

        self.angle2_label.grid(row=2, column=1, sticky="W")
        self.angle2_time_label.grid(row=3, column=1, sticky="W")

        self.fastest_angle_label.grid(row=4, column=0, sticky="W")
        self.fastest_time_label.grid(row=5, column=0, sticky="W")



    
    def add_graph_frame(self):
        graph_frame = ctk.CTkFrame(self.main_window)
        graph_frame.grid(row=0, column=1)

        fig = matplotlib.figure.Figure()
        sub_plot = fig.add_subplot()


        label_projectile = ctk.CTkLabel(graph_frame, text="Trajectory of projectile:", font=("Courier", 10)).grid(row=0, column=0)

        canvas = FigureCanvasTkAgg(fig, master=graph_frame)
        canvas.get_tk_widget().grid(row=1, column=0)



        print("graph_fastest_angle:", self.graph_fastest_angle, " graph_fastest_time:",self.graph_fastest_time)
        ctk.CTkButton(graph_frame, text="Plot Graph", command=lambda: plot(sub_plot,canvas, float(self.entry_speed.get()), float(self.entry_vector_y.get()), self.graph_fastest_angle, self.graph_fastest_time)).grid(row=2, column=0)
        ctk.CTkButton(graph_frame, text="End ", command=self.EndPrg).grid(row=3, column=0)

        toolbar = NavigationToolbar2Tk(canvas, graph_frame, pack_toolbar=False)
        toolbar.update()
        toolbar.grid(row=4, column=0)


    def EndPrg(self):
        sys.exit()

    def projectile_calculate(self):
        try:
            print("projectile_calculate")
            speed = float(self.entry_speed.get())
            vector_x = float(self.entry_vector_x.get())
            vector_y = float(self.entry_vector_y.get())
            vector_z = float(self.entry_vector_z.get())

            magnitude = math.sqrt(vector_x*vector_x + vector_y*vector_y + vector_z*vector_z)
            self.magnitude_label.configure(text=f"Magnitude: {magnitude:.2f}")

            direction_result = calculate_direction(vector_x, vector_z)
            self.direction_label.configure(text=direction_result)

            angle_1, angle_2, time_1, time_2 = calculate_angle_and_time(self.gravity, speed, vector_x, vector_y, vector_z)

            self.angle1_label.configure(text=f"Angle 1: {angle_1:.1f}°")
            self.angle1_time_label.configure(text=f"Time of action: {time_1:.1f}s")

            self.angle2_label.configure(text=f"Angle 2 {angle_2:.1f}°")
            self.angle2_time_label.configure(text=f"Time of action: {time_2:.1f}s")
            
            fastest_angle, fastest_time = recommended_angle(time_2, time_1, angle_2, angle_1)
            self.fastest_angle_label.configure(text=f"Recommended angle: {fastest_angle:.1f}°")
            self.fastest_time_label.configure(text=f"Recommended time: {fastest_time:.1f}s")

            print("fastest_angle:", fastest_angle, " fastest_time:",fastest_time)
            self.graph_fastest_angle = fastest_angle
            self.graph_fastest_time = fastest_time

        except ValueError:
            self.magnitude_label.configure(text="Target too far away")


    def projectile_delete(self):
        print(self.entry_projectile_name.get())
        
        # delete projectile from database using projectiles object
        self.projectiles.delete_row(self.entry_projectile_name.get())
        
        # read projectiles from database
        projectile_list = self.projectiles.read_all()
        projectile_name_list  = [x[0] for x in projectile_list]
        # print(projectile_name_list)
        
        # refresh projectile combobox
        self.combobox.configure(values=projectile_name_list)

    def projectile_save(self):
        print(self.entry_projectile_name.get())
        print(self.entry_speed.get())
        
        # read projectile from database using entry_projectile_name value
        projectile_check = self.projectiles.read_row(self.entry_projectile_name.get())
        print(projectile_check)
        
        
        if projectile_check: 
            # projectile exists in the database, we will update the database using screen values
            self.projectiles.update_row(self.entry_projectile_name.get(),
                                self.entry_speed.get(),
                                self.entry_vector_x.get(),
                                self.entry_vector_y.get(),
                                self.entry_vector_z.get()
                                )
        else:
            # projectile not exists in the database, we will insert new row using screen values
            self.projectiles.insert_row(self.entry_projectile_name.get(),
                                self.entry_speed.get(),
                                self.entry_vector_x.get(),
                                self.entry_vector_y.get(),
                                self.entry_vector_z.get()
                                )
        
        # read all projectiles from database
        projectile_list = self.projectiles.read_all()
        # create projectile_name_list from projectile names 
        projectile_name_list  = [prj[0] for prj in projectile_list]
        print(projectile_name_list)

        # refresh projectile combobox
        self.combobox.configure(values=projectile_name_list)


    def projectile_combobox_refresh(self, choice):
        print("combobox dropdown clicked:", choice)
        # read projectiles from database
        projectile_list = self.projectiles.read_all()
        
        for prj in projectile_list:
            # loop projectiles   
            print(prj[0] ,  choice)
            if prj[0] == choice:
                # if projectile name is same as choosen projectile, update screen with database values
                self.entry_projectile_name.delete(0,tk.END)
                self.entry_projectile_name.insert(0, prj[0])

                self.entry_speed.delete(0,tk.END)
                self.entry_speed.insert(0, prj[2])
                self.entry_vector_x.delete(0,tk.END)
                self.entry_vector_x.insert(0, prj[3])
                self.entry_vector_y.delete(0,tk.END)
                self.entry_vector_y.insert(0, prj[4])
                self.entry_vector_z.delete(0,tk.END)
                self.entry_vector_z.insert(0, prj[5])
