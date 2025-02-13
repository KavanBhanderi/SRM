from tkinter import *
from tkinter import messagebox
import os
import subprocess

class LoginForm:
    def __init__(self, root):
        self.root = root
        self.root.title("Login Form")
        self.root.geometry("450x350+500+200")  # Increased width and height
        self.root.config(bg="#e6f7ff")  # Changed background color

        # Title
        title = Label(self.root, text="Login", font=("Arial", 24, "bold"), bg="#e6f7ff", fg="#007acc")
        title.pack(pady=30)

        # Username/Email Label and Entry
        lbl_username = Label(self.root, text="Username/Email:", font=("Arial", 14), bg="#e6f7ff")
        lbl_username.place(x=50, y=100)
        self.txt_username = Entry(self.root, font=("Arial", 14), bg="#ffffff", bd=2, relief=SOLID)
        self.txt_username.place(x=200, y=100, width=200)

        # Password Label and Entry
        lbl_password = Label(self.root, text="Password:", font=("Arial", 14), bg="#e6f7ff")
        lbl_password.place(x=50, y=150)
        self.txt_password = Entry(self.root, font=("Arial", 14), bg="#ffffff", bd=2, relief=SOLID, show="*")
        self.txt_password.place(x=200, y=150, width=200)

        # Login Button
        btn_login = Button(self.root, text="Login", font=("Arial", 14, "bold"), bg="#007acc", fg="white", command=self.login)
        btn_login.place(x=175, y=220, width=120, height=40)

    def login(self):
        username = self.txt_username.get()
        password = self.txt_password.get()

        if username == "" or password == "":
            messagebox.showerror("Error", "All fields are required")
        elif username == "admin" and password == "12345":  # Example credentials
            messagebox.showinfo("Login Success", "Welcome!")
            self.root.destroy()  # Close the login window
            subprocess.run(["python", "Dashboard.py"]) # Open the main dashboard
        else:
            messagebox.showerror("Error", "Invalid Username or Password")

# Main Execution
if __name__ == "__main__":
    root = Tk()
    app = LoginForm(root)
    root.mainloop()