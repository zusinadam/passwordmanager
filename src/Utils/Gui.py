import tkinter as tk
from tkinter import messagebox
from Utils.Database import Database, User
from Utils.Password import Password

class PasswordManagerGUI:
    ''' Class shows application user interface and use utils class to handle application logic '''

    def __init__(self):
        ''' Initialize class and show welcome window od the Application'''

        # Intialize connection to database
        self.db = Database(database_name='menadzerhasel')
        self.db.connect()
        self.user = None

        # Set main interface gui option
        self.root = tk.Tk()
        self.root.title('Password Manager')
        self.root.configure(bg='#1A1A1A')

        # Set defualt screen size
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = int(screen_width * 3 / 4)
        window_height = int(screen_height * 3 / 4)
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f'{window_width}x{window_height}+{x}+{y}')
        self.frame = None

        self.show_login(True)

        # Start main loop of the program
        self.root.mainloop()

    def logout(self):
        if not self.user == None:
            self.user[1].logout()
            self.user == None

        self.show_login(True)

    def exit(self):
        """ End execution of application """
        if not self.user == None:
            self.user[1].logout()
        self.db.disconnect()
        exit(0) 

    def show_login(self, destroy = True):
        """ Draw login frame """
        
        if destroy and self.frame != None:
            self.frame.destroy()
            self.frame = None

        if self.frame == None:
            # Set default frame background color
            self.frame = tk.Frame(self.root, bg='#1A1A1A')
            self.frame.pack(expand=True)

            # Frame responsible used to center fields in frame
            self.center_frame = tk.Frame(self.frame, bg='#1A1A1A')
            self.center_frame.pack(pady=50)

            # Set fields used for login
            self.username_label = tk.Label(self.center_frame, text='Username:', bg='#1A1A1A', fg='white')
            self.username_label.grid(row=0, column=0, pady='7')
            self.username_entry = tk.Entry(self.center_frame)
            self.username_entry.grid(row=0, column=1, pady='7', columnspan=2)
            self.password_label = tk.Label(self.center_frame, text='Password:', bg='#1A1A1A', fg='white')
            self.password_label.grid(row=1, column=0, pady='7')
            self.password_entry = tk.Entry(self.center_frame, show='*')
            self.password_entry.grid(row=1, column=1, pady='7', columnspan=2)
            self.login_button = tk.Button(self.center_frame, text='Login', command=self.login, bg='#1A1A1A', fg='white', padx='25')
            self.login_button.grid(row=2, column=1, pady='3', padx='10')
            self.register_button = tk.Button(self.center_frame, text='Register', command=self.show_register, bg='#1A1A1A', fg='white', padx='19')
            self.register_button.grid(row=3, column=1, pady='3', padx='10')
            self.exit_button = tk.Button(self.center_frame, text='Exit', command=self.exit, bg='#1A1A1A', fg='white', padx='31')
            self.exit_button.grid(row=4, column=1, pady='3', padx='10')

    def login(self, show=False):
        """ Handle login menu operations """

        self.show_login(False)

        username = self.username_entry.get()
        password = self.password_entry.get()

        if not self.db.is_connected():
            self.db.reconnect()

        # Check if application is connected do database
        if self.db.is_connected():

            # Try login user
            self.user = User.login(username, password, self.db.connection_engine)
            
            # Check if user is logged
            if self.user[0]:
                self.show_menu(True)

            # Show error message
            else:
                messagebox.showwarning('Login Failed', self.user[1])
                self.user = None
        else:
            messagebox.showerror('Database Error', 'Could not connect to the database')

    def show_register(self, destroy = True):
        """ Draw register frame """
        
        if destroy and self.frame != None:
            self.frame.destroy()
            self.frame = None

        if self.frame == None:
            # Set default frame background color
            self.frame = tk.Frame(self.root, bg='#1A1A1A')
            self.frame.pack(expand=True)

            # Frame responsible used to center fields in frame
            self.center_frame = tk.Frame(self.frame, bg='#1A1A1A')
            self.center_frame.pack(pady=50)

            # Set fields used for register
            self.username_label = tk.Label(self.center_frame, text='Username:', bg='#1A1A1A', fg='white')
            self.username_label.grid(row=0, column=0, pady='7')
            self.username_entry = tk.Entry(self.center_frame)
            self.username_entry.grid(row=0, column=1, pady='7', columnspan=2)
            self.email_label = tk.Label(self.center_frame, text='Email:', bg='#1A1A1A', fg='white')
            self.email_label.grid(row=1, column=0, pady='7')
            self.email_entry = tk.Entry(self.center_frame)
            self.email_entry.grid(row=1, column=1, pady='7', columnspan=2)
            self.password_label = tk.Label(self.center_frame, text='Password:', bg='#1A1A1A', fg='white')
            self.password_label.grid(row=2, column=0, pady='7')
            self.password_entry = tk.Entry(self.center_frame, show='*')
            self.password_entry.grid(row=2, column=1, pady='7', columnspan=2)
            self.password2_label = tk.Label(self.center_frame, text='Retry password:', bg='#1A1A1A', fg='white')
            self.password2_label.grid(row=3, column=0, pady='7')
            self.password2_entry = tk.Entry(self.center_frame, show='*')
            self.password2_entry.grid(row=3, column=1, pady='7', columnspan=2)            
            self.register_button = tk.Button(self.center_frame, text='Register', command=self.register, bg='#1A1A1A', fg='white', padx='19')
            self.register_button.grid(row=4, column=1, pady='3', padx='10')
            self.back_button = tk.Button(self.center_frame, text='Back', command=self.show_login, bg='#1A1A1A', fg='white', padx='31')
            self.back_button.grid(row=5, column=1, pady='3', padx='10')

    def register(self):
        """ Handle register user operations """

        self.show_register(False)

        username = self.username_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        password2 = self.password2_entry.get()

        # Check if application is connected do database
        if self.db.is_connected():

            # Try register user
            self.user = User.register(username, email, password, password2, self.db.connection_engine)
            
            # Check if user was register
            if self.user[0]:
                self.user = None
                self.show_register(True)
                messagebox.showinfo('Success', 'User ' + username + ' was registered.')

            # Show user username or password is incorrect
            else:
                self.show_register(False)
                messagebox.showwarning('Register Failed', self.user[1])
        else:
            messagebox.showerror('Database Error', 'Could not connect to the database.')
            self.logout()

    def show_menu(self, destroy = True):

        if self.user == None or not self.db.is_connected():
            messagebox.showwarning('Session', 'User is not logged in.')
            self.logout()

        if destroy and self.frame != None:
            self.frame.destroy()
            self.frame = None

        if self.frame == None:
            # Set default frame background color
            self.frame = tk.Frame(self.root, bg='#1A1A1A')
            self.frame.pack(expand=True)

            # Frame responsible used to center fields in frame
            self.center_frame = tk.Frame(self.frame, bg='#1A1A1A')
            self.center_frame.pack(pady=50)

            # Set fields used for menu 
            #self.store_password_button = tk.Button(self.center_frame, text='Store password', command=self.register, bg='#1A1A1A', fg='white', padx='19')
            #self.store_password_button.grid(row=0, column=1, pady='3', padx='20')
            #self.retrive_password_button = tk.Button(self.center_frame, text='Retrive password', command=self.register, bg='#1A1A1A', fg='white', padx='19')
            #self.retrive_password_button.grid(row=1, column=1, pady='3', padx='18')          
            self.generate_password_button = tk.Button(self.center_frame, text='Generate password', command=self.show_generate_password, bg='#1A1A1A', fg='white', padx='19')
            self.generate_password_button.grid(row=2, column=1, pady='3', padx='10')
            self.change_password_button = tk.Button(self.center_frame, text='Change password', command=self.show_change_password, bg='#1A1A1A', fg='white', padx='19')
            self.change_password_button.grid(row=3, column=1, pady='3', padx='11')
            self.logout_button = tk.Button(self.center_frame, text='Logout', command=self.logout, bg='#1A1A1A', fg='white', padx='31')
            self.logout_button.grid(row=5, column=1, pady='3', padx='10')   

    @staticmethod
    def toggle_checkbox(checkbox: tk.Checkbutton, var: tk.BooleanVar) -> None:
        """ Change checkbox state and toogle value """
        current_state = var.get()
        var.set(not current_state)
        checkbox.configure(state=tk.NORMAL if current_state else tk.ACTIVE)

    def show_generate_password(self, destroy = True):
        """ Draw generate password frame """

        if self.user == None or not self.db.is_connected():
            messagebox.showwarning('Session', 'User is not logged in.')
            self.logout()

        if destroy and self.frame != None:
            self.frame.destroy()
            self.frame = None

        if self.frame == None:
            # Set default frame background color
            self.frame = tk.Frame(self.root, bg='#1A1A1A')  
            self.frame.pack(expand=True)

            # Frame responsible used to center fields in frame
            self.center_frame = tk.Frame(self.frame, bg='#1A1A1A')
            self.center_frame.pack(pady=50)

            # Set fields for generate password frame
            self.min_label = tk.Label(self.center_frame, text='Minimal length:', bg='#1A1A1A', fg='white')
            self.min_label.grid(row=0, column=0, pady='7')
            self.min_entry = tk.Entry(self.center_frame)
            self.min_entry.insert(0, '8')
            self.min_entry.grid(row=0, column=1, pady='7', columnspan=2)
            self.max_label = tk.Label(self.center_frame, text='Maximal length:', bg='#1A1A1A', fg='white')
            self.max_label.grid(row=1, column=0, pady='7')
            self.max_entry = tk.Entry(self.center_frame)
            self.max_entry.insert(0, '20')
            self.max_entry.grid(row=1, column=1, pady='7', columnspan=2)
            self.letters_label = tk.Label(self.center_frame, text='Contains letters', bg='#1A1A1A', fg='white')
            self.letters_label.grid(row=2, column=0)
            self.letters = tk.BooleanVar(value=True)
            self.letters_checkbox = tk.Checkbutton(self.center_frame, variable=self.letters, state='normal', bg='#1A1A1A', activebackground='#1A1A1A', offvalue= False, onvalue=True)
            self.letters_checkbox.grid(row=2, column=1, pady='3', padx='10') 
            self.lowercase_label = tk.Label(self.center_frame, text='Contains lowercase', bg='#1A1A1A', fg='white')
            self.lowercase_label.grid(row=3, column=0)
            self.lowercase = tk.BooleanVar(value=True)
            self.lowercase_checkbox = tk.Checkbutton(self.center_frame, variable=self.lowercase, state='normal', bg='#1A1A1A', activebackground='#1A1A1A', offvalue= False, onvalue=True)
            self.lowercase_checkbox.grid(row=3, column=1, pady='3', padx='10') 
            self.uppercase_label = tk.Label(self.center_frame, text='Contains uppercase', bg='#1A1A1A', fg='white')
            self.uppercase_label.grid(row=4, column=0)
            self.uppercase = tk.BooleanVar(value=True)
            self.uppercase_checkbox = tk.Checkbutton(self.center_frame, variable=self.uppercase, state='normal', bg='#1A1A1A', activebackground='#1A1A1A', offvalue= False, onvalue=True)
            self.uppercase_checkbox.grid(row=4, column=1, pady='3', padx='10') 
            self.digits_label = tk.Label(self.center_frame, text='Contains digits', bg='#1A1A1A', fg='white')
            self.digits_label.grid(row=5, column=0)
            self.digits = tk.BooleanVar(value=True)
            self.digits_checkbox = tk.Checkbutton(self.center_frame, variable=self.digits, state='normal', bg='#1A1A1A', activebackground='#1A1A1A', offvalue= False, onvalue=True)
            self.digits_checkbox.grid(row=5, column=1, pady='3', padx='10') 
            self.punctuation_label = tk.Label(self.center_frame, text='Contains punctuations', bg='#1A1A1A', fg='white')
            self.punctuation_label.grid(row=6, column=0)
            self.punctuation = tk.BooleanVar(value=True)
            self.punctuation_checkbox = tk.Checkbutton(self.center_frame, variable=self.punctuation, state='normal', bg='#1A1A1A', activebackground='#1A1A1A', offvalue= False, onvalue=True)
            self.punctuation_checkbox.grid(row=6, column=1, pady='3', padx='10') 
            self.reccuring_type_label = tk.Label(self.center_frame, text='Reccuring type alowed', bg='#1A1A1A', fg='white')
            self.reccuring_type_label.grid(row=7, column=0)
            self.reccuring_type = tk.BooleanVar(value=True)
            self.reccuring_type_checkbox = tk.Checkbutton(self.center_frame, variable=self.reccuring_type, state='normal', bg='#1A1A1A', activebackground='#1A1A1A', offvalue= False, onvalue=True)
            self.reccuring_type_checkbox.grid(row=7, column=1, pady='3', padx='10') 
            self.generate_password_button = tk.Button(self.center_frame, text='Generate Password', command=self.generate_password, bg='#1A1A1A', fg='white')
            self.generate_password_button.grid(row=8, column=1, pady='3', padx='10') 
            self.back_button = tk.Button(self.center_frame, text='Back', command=self.show_menu, bg='#1A1A1A', fg='white', padx='31')
            self.back_button.grid(row=9, column=1, pady='3', padx='10')   

    def generate_password(self):
        """ Handle generate password operations """
        
        if self.user == None or not self.db.is_connected():
            messagebox.showwarning('Session', 'User is not logged in.')
            self.logout()

        self.show_generate_password(False)

        min_length = self.min_entry.get()
        max_length = self.max_entry.get()
        letters = self.letters.get()
        lowercase = self.lowercase.get()
        uppercase = self.uppercase.get()
        digits =  self.digits.get()
        punctuations = self.punctuation.get()
        reccuring_type = self.reccuring_type.get()

        # Check if application is connected do database
        if self.db.is_connected():

            # Try generate password
            try:
                password =  Password.generate(min_length, max_length, letters, lowercase, uppercase, digits, punctuations, reccuring_type)
                self.show_generate_password(False)
                messagebox.showinfo('Generated password', password)

            # Show criteria is not correct
            except ValueError as e:
                self.show_generate_password(False)
                messagebox.showwarning('Generate Password Failed', e.args)

        else:
            messagebox.showerror('Database Error', 'Could not connect to the database.')
            self.logout()

    def show_change_password(self, destroy = True):
        """ Draw change password frame """
        
        if self.user == None or not self.db.is_connected():
            messagebox.showwarning('Session', 'User is not logged in.')
            self.logout()

        if destroy and self.frame != None:
            self.frame.destroy()
            self.frame = None

        if self.frame == None:

            # Set default background color
            self.frame = tk.Frame(self.root, bg='#1A1A1A')
            self.frame.pack(expand=True)

            # Frame responsible used to center fields in frame
            self.center_frame = tk.Frame(self.frame, bg='#1A1A1A')
            self.center_frame.pack(pady=50)

            # Set fields used for change password
            self.password_label = tk.Label(self.center_frame, text='Old password:', bg='#1A1A1A', fg='white')
            self.password_label.grid(row=0, column=0, pady='7')
            self.password_entry = tk.Entry(self.center_frame, show='*')
            self.password_entry.grid(row=0, column=1, pady='7', columnspan=2)
            self.password1_label = tk.Label(self.center_frame, text='New password:', bg='#1A1A1A', fg='white')
            self.password1_label.grid(row=1, column=0, pady='7')
            self.password1_entry = tk.Entry(self.center_frame, show='*')
            self.password1_entry.grid(row=1, column=1, pady='7', columnspan=2) 
            self.password2_label = tk.Label(self.center_frame, text='Retry new password:', bg='#1A1A1A', fg='white')
            self.password2_label.grid(row=2, column=0, pady='7')
            self.password2_entry = tk.Entry(self.center_frame, show='*')
            self.password2_entry.grid(row=2, column=1, pady='7', columnspan=2)            
            self.register_button = tk.Button(self.center_frame, text='Change password', command=self.change_password, bg='#1A1A1A', fg='white', padx='19')
            self.register_button.grid(row=3, column=1, pady='3', padx='10')
            self.back_button = tk.Button(self.center_frame, text='Back', command=self.show_menu, bg='#1A1A1A', fg='white', padx='31')
            self.back_button.grid(row=4, column=1, pady='3', padx='10')

    def change_password(self):
        """ Handle register user operations """
        
        if self.user == None or not self.db.is_connected():
            messagebox.showwarning('Session', 'User is not logged in.')
            self.logout()

        self.show_change_password(False)

        password = self.password_entry.get()
        password1 = self.password1_entry.get()
        password2 = self.password2_entry.get()

        # Check if application is connected do database
        if self.db.is_connected():

            # Try change  user password
            x = self.user[1].change_password(old_password=password, new_password=password1, new_password2=password2)
            
            # Check if user password changed
            if self.user[0]:
                self.user = None
                self.show_change_password(True)
                messagebox.showinfo('Success', 'User password was changed.')

            # Show user username or password is incorrect
            else:
                self.show_change_password(False)
                messagebox.showwarning('Change Password Failed', self.user[1])
        else:
            messagebox.showerror('Database Error', 'Could not connect to the database.')
            self.logout()

if __name__ == '__main__':
    PasswordManagerGUI()