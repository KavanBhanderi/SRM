from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
import sqlite3

class ResultClass:
    def __init__(self, root):
        self.root = root
        self.root.title("Manage Student Details")
        self.root.geometry("1200x480+80+170")
        self.root.config(bg="white")
        self.root.focus_force()
    
        # ===== Title =====
        title = Label(self.root, text="Add Student Results", font=("goudy old style", 20, "bold"), bg="orange", fg="black").place(x=10, y=15, width=1180, height=35)
        # ===== variables =====
        self.var_roll = StringVar()
        self.var_name = StringVar()
        self.var_course = StringVar()
        self.var_marks = StringVar()
        self.var_full_marks = StringVar()
        self.roll_list =[]
       
        # ===== Widgets =====
        lbl_select = Label(self.root,text="Select Student",font=("goudy old style", 20, "bold"),bg="white").place(x=50,y=100)
        lbl_name = Label(self.root,text="Name",font=("goudy old style", 20, "bold"),bg="white").place(x=50,y=160)
        lbl_course = Label(self.root,text="Course",font=("goudy old style", 20, "bold"),bg="white").place(x=50,y=220)
        lbl_mark_ob = Label(self.root,text="Mark Obtained ",font=("goudy old style", 20, "bold"),bg="white").place(x=50,y=280)
        lbl_full_marks = Label(self.root,text="Full Marks",font=("goudy old style", 20, "bold"),bg="white").place(x=50,y=340)

        self.txt_student=ttk.Combobox(self.root, textvariable=self.var_roll,values=self.roll_list,font=("goudy old style", 15),state='readonly',justify=CENTER)
        self.txt_student.place(x=280, y=100, width=200)
        self.txt_student.set("Select Student")
        self.fetch_roll() 
        btn_search = Button(self.root,text="Search",font=("goudy old styl",15,"bold"),bg="blue",fg="white",cursor="hand2",command=self.search).place(x=500,y=100,width=100,height=28)

        txt_name = Entry(self.root,textvariable=self.var_name,font=("goudy old styl",20),bg="white",state="readonly").place(x=280,y=160,width=320)
        txt_course = Entry(self.root,textvariable=self.var_course,font=("goudy old styl",20),bg="white",state="readonly").place(x=280,y=220,width=320)
        txt_marks = Entry(self.root,textvariable=self.var_marks,font=("goudy old styl",20),bg="white").place(x=280,y=280,width=320)
        txt_full_marks = Entry(self.root,textvariable=self.var_full_marks,font=("goudy old styl",20),bg="white").place(x=280,y=340,width=320)
        
        # ===== Buttons =====
        self.btn_add=Button(self.root, text="Save", font=("goudy old style", 15, "bold"), bg="green", fg="white",activebackground="green", cursor="hand2",command=self.insert)
        self.btn_add.place(x=300,y=420,width=110,height=40)
        self.btn_clear=Button(self.root, text="Clear", font=("goudy old style", 15, "bold"), bg="gray", fg="white", cursor="hand2",command=self.clear)
        self.btn_clear.place(x=430, y=420, width=110, height=40)

        # ===== Image =====
        image_path = os.path.join("Image", "result.jpg")
        image = Image.open(image_path)
        image = image.resize((500, 300)) 
        self.logo_dash = ImageTk.PhotoImage(image)
        self.lbl_bg=Label(self.root,image=self.logo_dash).place(x=650,y=100)


        # ==== Function =====
    def clear(self):
        self.var_roll.set("Select Student")
        self.var_name.set("")
        self.var_course.set("")
        self.var_marks.set("")
        self.var_full_marks.set("")
    
    def fetch_roll(self):
        con = sqlite3.connect("rms.db")
        cur = con.cursor()
        cur.execute("SELECT roll FROM student")
        rows = cur.fetchall() 
        self.roll_list = [row[0] for row in rows]  
        self.txt_student['values'] = self.roll_list 

    def insert(self):
        # Connect to the database
        con = sqlite3.connect("rms.db")
        cur = con.cursor()
        roll = self.var_roll.get().strip()
        name = self.var_name.get().strip()
        course = self.var_course.get().strip()
        mark = self.var_marks.get().strip()
        full_mark = self.var_full_marks.get().strip()

            # Input validation
        if not roll or not name or not course or not mark or not full_mark:
                messagebox.showerror("Error", "All fields are required.", parent=self.root)
                return

        if not mark.isdigit() or not full_mark.isdigit():
                messagebox.showerror("Error", "Marks and Full Marks must be valid numbers.", parent=self.root)
                return

        mark = int(mark)
        full_mark = int(full_mark)

        if not (0 <= mark <= full_mark):
                messagebox.showerror("Error", f"Marks must be between 0 and {full_mark}.", parent=self.root)
                return

            # Check if the roll number and course already exist
        cur.execute("SELECT * FROM result WHERE roll=? AND course=?", (roll, course))
        if cur.fetchone():
            messagebox.showerror("Error", "A result with this roll number already exists.", parent=self.root)
            return

            # Insert the record into the database
        per = (mark * 100) / full_mark
        cur.execute(
                "INSERT INTO result (roll, name, course, marks_ob, full_marks, per) VALUES (?, ?, ?, ?, ?, ?)",
                (roll, name, course, mark, full_mark, per),
            )
        con.commit()
        messagebox.showinfo("Success", "Result inserted successfully.", parent=self.root)
        self.clear()

    def search(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        cur.execute("SELECT name,course FROM student WHERE roll LIKE ?", ('%' + self.var_roll.get().strip() + '%',))
        row = cur.fetchone()
        if row != None:
                self.var_name.set(row[0])
                self.var_course.set(row[1])
        else:
            messagebox.showinfo("No Results", "No record found for the entered roll number.", parent=self.root)
   

if __name__ == "__main__" :
    root = Tk()
    obj = ResultClass(root)
    root.mainloop()