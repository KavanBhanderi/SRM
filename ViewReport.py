from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
import sqlite3

class ViewReportClass:
    def __init__(self, root):
        self.root = root
        self.root.title("Manage Student Details")
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = 1200
        window_height = 480
        position_top = int(screen_height / 2 - window_height / 2)
        position_left = int(screen_width / 2 - window_width / 2)
        self.root.geometry(f"{window_width}x{window_height}+{position_left}+{position_top}")
        self.root.config(bg="white")
        self.root.resizable(False, False)
        self.root.focus_force()
    
        # ===== Title =====
        title = Label(self.root, text="View Student Results", font=("goudy old style", 20, "bold"), bg="orange", fg="black").place(x=10, y=15, width=1180, height=35)
        
        self.var_search = StringVar()
        self.var_id =""
        lbl_search = Label(self.root,text="Search By Roll No.",font=("goudy old style", 20, "bold"),bg="white").place(x=300,y=100)
        txt_search = Entry(self.root,textvariable=self.var_search,font=("goudy old style", 20),bg="white").place(x=550,y=100,width=150)
        btn_search = Button(self.root,text="Search",font=("goudy old styl",15,"bold"),bg="blue",fg="white",cursor="hand2",command=self.search).place(x=720,y=100,width=100,height=35)
        btn_clear = Button(self.root,text="Clear",font=("goudy old styl",15,"bold"),bg="gray",fg="white",cursor="hand2",command=self.clear).place(x=830,y=100,width=100,height=35)

       # ===== Result Label =====
        lbl_roll = Label(self.root,text="Roll No.",font=("goudy old style", 15, "bold"),bg="white",bd=2,relief=GROOVE).place(x=150,y=230,width=150,height=50)
        lbl_name =Label(self.root,text="Name",font=("goudy old style", 15, "bold"),bg="white",bd=2,relief=GROOVE).place(x=300,y=230,width=150,height=50)
        lbl_course = Label(self.root,text="Course",font=("goudy old style", 15, "bold"),bg="white",bd=2,relief=GROOVE).place(x=450,y=230,width=150,height=50)
        lbl_marks = Label(self.root,text="Marks Obtained",font=("goudy old style", 15, "bold"),bg="white",bd=2,relief=GROOVE).place(x=600,y=230,width=150,height=50)
        lbl_full = Label(self.root,text="Total Marks",font=("goudy old style", 15, "bold"),bg="white",bd=2,relief=GROOVE).place(x=750,y=230,width=150,height=50)
        lbl_per = Label(self.root,text="Percentage",font=("goudy old style", 15, "bold"),bg="white",bd=2,relief=GROOVE).place(x=900,y=230,width=150,height=50)

        self.roll = Label(self.root,font=("goudy old style", 15, "bold"),bg="white",bd=2,relief=GROOVE)
        self.roll.place(x=150,y=280,width=150,height=50)
        self.name =Label(self.root,font=("goudy old style", 15, "bold"),bg="white",bd=2,relief=GROOVE)
        self.name.place(x=300,y=280,width=150,height=50)
        self.course = Label(self.root,font=("goudy old style", 15, "bold"),bg="white",bd=2,relief=GROOVE)
        self.course.place(x=450,y=280,width=150,height=50)
        self.marks = Label(self.root,font=("goudy old style", 15, "bold"),bg="white",bd=2,relief=GROOVE)
        self.marks.place(x=600,y=280,width=150,height=50)
        self.full = Label(self.root,font=("goudy old style", 15, "bold"),bg="white",bd=2,relief=GROOVE)
        self.full.place(x=750,y=280,width=150,height=50)
        self.per = Label(self.root,font=("goudy old style", 15, "bold"),bg="white",bd=2,relief=GROOVE)
        self.per.place(x=900,y=280,width=150,height=50)

        btn_delete = Button(self.root,text="Delete",font=("goudy old styl",15,"bold"),bg="red",fg="white",cursor="hand2",command=self.delete).place(x=500,y=350,width=150,height=35)

        # ===== Function =====
    def search(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        if self.var_search.get() == "":
             messagebox.showerror("Error","Roll No. Should Be Required",parent=self.root)
        else:
            cur.execute("SELECT * FROM result WHERE roll LIKE ?", ('%' + self.var_search.get().strip() + '%',))
            row = cur.fetchone()
            if row != None:
                    self.var_id =row[0]
                    self.roll.config(text=row[1])
                    self.name.config(text=row[2])
                    self.course.config(text=row[3])
                    self.marks.config(text=row[4])
                    self.full.config(text=row[5])
                    self.per.config(text=row[6])
            else:
                messagebox.showinfo("No Results", "No record found for the entered roll number.", parent=self.root)
   
    def clear(self):
            self.var_id=""
            self.roll.config(text="")
            self.name.config(text="")
            self.course.config(text="")
            self.marks.config(text="")
            self.full.config(text="")
            self.per.config(text="")
            self.var_search.set("")

    def delete(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        if self.var_id =="":
            messagebox.showerror("Error","Search Student Result First",parent=self.root)
        else:
            cur.execute("select * from result where rid=?", (self.var_id,))
            row = cur.fetchone()
            if row == None:
                messagebox.showerror("Error","Invalid Student Result",parent=self.root)
            else:
                op = messagebox.askyesno("Confirm","Do You Really Want To Delete?",parent=self.root)
                if op==True:
                    cur.execute("delete from result where rid=?",(self.var_id,))
                    con.commit()
                    messagebox.showinfo("Delete","Result Deleted Successfully",parent=self.root)
                    self.clear()

if __name__ == "__main__" :
    root = Tk()
    obj = ViewReportClass(root)
    root.mainloop()