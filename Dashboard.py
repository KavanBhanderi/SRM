import os
from tkinter import *
from PIL import Image,ImageTk
import time
import sqlite3
from tkinter import ttk, messagebox
from Course import CourseClass
from Student import StudentManagement
from Result import ResultClass
from ViewReport import ViewReportClass
from Login import LoginForm

class RMS:
    def __init__(self,root):
        self.root=root
        self.root.title("Student Result Management")
        window_width = 1366
        window_height = 768  
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)
        self.root.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")
        self.root.resizable(False, False)
        self.root.config(bg="white")

        # ===== Image =====
        image_path = os.path.join("Image", "student3_117884.png")
        image = Image.open(image_path)
        image = image.resize((40, 40)) 
        self.logo_dash = ImageTk.PhotoImage(image)
    
        # ===== Title =====
        title=Label(self.root,text="Student Result Management System",padx=10,compound=LEFT,image=self.logo_dash,font=("goudy old style",20,"bold"),bg="#033054",fg="white").place(x=0,y=0,relwidth=1,height=50)

        # ===== Menu =====
        M_Frame = LabelFrame(self.root,text="Menus",font=("times new roman",15),bg="white")
        M_Frame.place(x=10,y=70,relwidth=0.99,height=70)

        btn_course = Button(M_Frame,text="Course",font=("goudy old style ",15,"bold"),bg="#0b5377",fg="white",cursor="hand2",command=self.add_course).place(x=20,y=5,width=200,height=30)
        btn_student = Button(M_Frame,text="Student",font=("goudy old style ",15,"bold"),bg="#0b5377",fg="white",cursor="hand2",command=self.add_student).place(x=240,y=5,width=200,height=30)
        btn_result = Button(M_Frame,text="Result",font=("goudy old style ",15,"bold"),bg="#0b5377",fg="white",cursor="hand2",command=self.add_result).place(x=460,y=5,width=200,height=30)
        btn_view = Button(M_Frame,text="View Student Result",font=("goudy old style ",15,"bold"),bg="#0b5377",fg="white",cursor="hand2",command=self.add_viewreport).place(x=680,y=5,width=200,height=30)
        btn_logout = Button(M_Frame,text="Logout",font=("goudy old style ",15,"bold"),bg="#0b5377",fg="white",cursor="hand2",command=self.logout).place(x=900,y=5,width=200,height=30)
        btn_exit = Button(M_Frame,text="Exit",font=("goudy old style ",15,"bold"),bg="#0b5377",fg="white",cursor="hand2",command=self.exit_app).place(x=1120,y=5,width=200,height=30)


         # ===== Footer =====
        footer=Label(self.root,text="SRMS - Student Result Management System \n Contact Us For Any Technical Issue : 992xxxxx64",font=("times new roman",12),bg="#262626",fg="white").pack(side=BOTTOM,fill=X)


        # ===== Image =====
        image_path = os.path.join("Image", "dashboard.jpeg")
        image = Image.open(image_path)
        image = image.resize((1280, 350)) 
        self.logo_dash = ImageTk.PhotoImage(image)
        self.lbl_bg=Label(self.root,image=self.logo_dash).place(x=40,y=180,width=1280,height=350)

        # ===== Update Details =====
        self.lbl_course = Label(self.root,text="Total Courses\n [ 0 ]",font=("goudy old style",20),bd=10,relief=RIDGE,bg="#e43b06",fg="white")
        self.lbl_course.place(x=40,y=550,width=300,height=100)
        self.total_course()
        

        self.lbl_student = Label(self.root,text="Total Student\n [ 0 ]",font=("goudy old style",20),bd=10,relief=RIDGE,bg="#0676ad",fg="white")
        self.lbl_student.place(x=520,y=550,width=300,height=100)
        self.total_student()
        
        self.lbl_result = Label(self.root,text="Total Result\n [ 0 ]",font=("goudy old style",20),bd=10,relief=RIDGE,bg="#038074",fg="white")
        self.lbl_result.place(x=1020,y=550,width=300,height=100)
        self.total_result()

    def add_course(self):
        if hasattr(self, 'new_win') and self.new_win.winfo_exists():
            self.new_win.destroy()
        self.new_win = Toplevel(self.root)
        self.new_obj = CourseClass(self.new_win)
    
    def add_student(self):
        if hasattr(self, 'new_win') and self.new_win.winfo_exists():
            self.new_win.destroy()
        self.new_win = Toplevel(self.root)
        self.new_obj = StudentManagement(self.new_win)

    def add_result(self):
        if hasattr(self, 'new_win') and self.new_win.winfo_exists():
            self.new_win.destroy()
        self.new_win = Toplevel(self.root)
        self.new_obj = ResultClass(self.new_win)


    def add_viewreport(self):
        if hasattr(self, 'new_win') and self.new_win.winfo_exists():
            self.new_win.destroy()
        self.new_win = Toplevel(self.root)
        self.new_obj = ViewReportClass(self.new_win)

    def total_course(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        cur.execute("select count(*) from course")
        count = cur.fetchone()[0]
        self.lbl_course.config(text=f"Total Courses\n [ {count} ]")
        self.lbl_course.after(200,self.total_course)
   
    def total_student(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        cur.execute("select count(*) from student")
        count = cur.fetchone()[0]
        self.lbl_student.config(text=f"Total Student\n [ {count} ]")
        self.lbl_student.after(200,self.total_student)
    
    def total_result(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        cur.execute("select count(*) from result")
        count = cur.fetchone()[0]
        self.lbl_result.config(text=f"Total Result\n [ {count} ]")
        self.lbl_result.after(200,self.total_result)

    def logout(self):
        """Simulate logout and redirect to login page."""
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.root.withdraw()
            login_window = Toplevel(self.root)
            login_obj = LoginForm(login_window)

    
    def exit_app(self):
        """Exit the application safely."""
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.root.destroy()

if __name__ == "__main__" :
    root = Tk()
    obj = RMS(root)
    root.mainloop()