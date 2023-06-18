import tkinter as tk
from tkinter import messagebox
from Database import Database
from Password import Password

class PasswordManagerGUI:
    def __init__(self):
        self.db = Database(database_name='menadzerhasel')
        self.logged_in = False

        self.root = tk.Tk()
        self.root.title("Password Manager")
        
        self.login_frame = tk.Frame(self.root)
        self.login_frame.pack()

        self.email_label = tk.Label(self.login_frame, text="Email:")
        self.email_label.grid(row=0, column=0)
        self.email_entry = tk.Entry(self.login_frame)
        self.email_entry.grid(row=0, column=1)

        self.password_label = tk.Label(self.login_frame, text="Password:")
        self.password_label.grid(row=1, column=0)
        self.password_entry = tk.Entry(self.login_frame, show="*")
        self.password_entry.grid(row=1, column=1)

        self.login_button = tk.Button(self.login_frame, text="Login", command=self.login)
        self.login_button.grid(row=2, columnspan=2)

        self.root.mainloop()

    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        # Sprawdź, czy użytkownik istnieje w bazie danych
        if self.db.is_connected():
            # Tutaj należy dokonać weryfikacji hasła z wykorzystaniem odpowiednich metod z klasy User
            # np. user = self.db.connection.query(User).filter_by(email=email).first()
            # if user and user.verify_password(password):
            if email == "admin" and password == "admin":
                self.logged_in = True
                self.show_passwords()
            else:
                messagebox.showerror("Login Failed", "Invalid email or password")
        else:
            messagebox.showerror("Database Error", "Could not connect to the database")

    def show_passwords(self):
        self.login_frame.destroy()

        self.passwords_frame = tk.Frame(self.root)
        self.passwords_frame.pack()

        self.generate_password_button = tk.Button(self.passwords_frame, text="Generate Password", command=self.generate_password)
        self.generate_password_button.pack()

        self.logout_button = tk.Button(self.passwords_frame, text="Logout", command=self.logout)
        self.logout_button.pack()

    def generate_password(self):
        if self.logged_in:
            password = Password.generate()
            messagebox.showinfo("Generated Password", f"Generated Password: {password}")
        else:
            messagebox.showerror("Not Logged In", "Please login first")

    def logout(self):
        self.logged_in = False
        self.passwords_frame.destroy()
        self.__init__()

if __name__ == "__main__":
    PasswordManagerGUI()
