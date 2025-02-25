import os
from tkinter import *
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import sqlite3
import mysql.connector
class CourseClass:
    def __init__(self,root):
        self.root=root
        self.root.title("Student Result Management")
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
        title=Label(self.root,text="Manage Course Details",font=("goudy old style",20,"bold"),bg="#033054",fg="white").place(x=10,y=15,width=1180,height=35)

        # ===== Variables =====
        self.var_course = StringVar()
        self.var_duration = StringVar()
        self.var_charges = StringVar()

        # ===== Widgets =====
        lbl_courseName = Label(self.root,text="Course Name",font=("goudy old styl",15,"bold"),bg="white").place(x=10,y=60)
        lbl_duration = Label(self.root,text="Duration",font=("goudy old styl",15,"bold"),bg="white").place(x=10,y=100)
        lbl_charges = Label(self.root,text="Charges",font=("goudy old styl",15,"bold"),bg="white").place(x=10,y=140)
        lbl_description = Label(self.root,text="Description",font=("goudy old styl",15,"bold"),bg="white").place(x=10,y=180)

        # ===== Entry Field =====
        self.txt_courseName = Entry(self.root,textvariable=self.var_course,font=("goudy old styl",15),bg="white")
        self.txt_courseName.place(x=150,y=60,width=200)
        txt_duration = Entry(self.root,textvariable=self.var_duration,font=("goudy old styl",15),bg="white").place(x=150,y=100,width=200)
        txt_charges = Entry(self.root,textvariable=self.var_charges,font=("goudy old styl",15),bg="white").place(x=150,y=140,width=200)
        self.txt_description = Text(self.root,font=("goudy old styl",15),bg="white")
        self.txt_description.place(x=150,y=180,width=500,height=100)

        # ===== Buttons =====
        self.btn_add = Button(self.root,text="Save",font=("goudy old styl",15,"bold"),bg="blue",fg="white",cursor="hand2",command=self.insert)
        self.btn_add.place(x=150,y=400,width=110,height=40)
        self.btn_update = Button(self.root,text="Update",font=("goudy old styl",15,"bold"),bg="green",fg="white",cursor="hand2",command=self.update)
        self.btn_update.place(x=270,y=400,width=110,height=40)
        self.btn_delete = Button(self.root,text="Delete",font=("goudy old styl",15,"bold"),bg="red",fg="white",cursor="hand2",command=self.delete)
        self.btn_delete.place(x=390,y=400,width=110,height=40)
        self.btn_clear = Button(self.root,text="Clear",font=("goudy old styl",15,"bold"),bg="gray",fg="white",cursor="hand2",command=self.clear)
        self.btn_clear.place(x=510,y=400,width=110,height=40)

        # ===== Search Panel =====
        self.var_search = StringVar()
        lbl_search_courseName = Label(self.root,text="Course Name ",font=("goudy old styl",15,"bold"),bg="white").place(x=720,y=60)
        txt_search_courseName = Entry(self.root,textvariable=self.var_search,font=("goudy old styl",15,"bold"),bg="white").place(x=870,y=60,width=180)
        btn_search = Button(self.root,text="Search",font=("goudy old styl",15,"bold"),bg="blue",fg="white",cursor="hand2",command=self.search).place(x=1070,y=60,width=120,height=28)

        # ===== Content =====
        self.C_Frame = Frame(self.root,relief=RIDGE)
        self.C_Frame.place(x=720,y=100,width=470,height=340)

        scrolly = Scrollbar(self.C_Frame,orient=VERTICAL)
        scrollx = Scrollbar(self.C_Frame,orient=HORIZONTAL)
        self.CourseTable = ttk.Treeview(self.C_Frame,columns=("cid","name","duration","charges","description"),xscrollcommand=scrollx.set,yscrollcommand=scrolly.set)
        
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.CourseTable.xview)
        scrolly.config(command=self.CourseTable.yview)
        
        self.CourseTable.heading("cid",text="Course ID")
        self.CourseTable.heading("name",text="Name")
        self.CourseTable.heading("duration",text="Duration")
        self.CourseTable.heading("charges",text="Charges")
        self.CourseTable.heading("description",text="Description")
        self.CourseTable["show"] = 'headings'
        self.CourseTable.column("cid",width=100)
        self.CourseTable.column("name",width=100)
        self.CourseTable.column("duration",width=100)
        self.CourseTable.column("charges",width=100)
        self.CourseTable.column("description",width=150)
        self.CourseTable.pack(fill=BOTH, expand=1)
        self.CourseTable.bind("<ButtonRelease-1>",self.get_data)
        self.show()

#========== CRUD FUNCTION ==========

    def search(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        cur.execute(f"select * from course where name LIKE '%{self.var_search.get()}%'")
        rows = cur.fetchall()
        self.CourseTable.delete(*self.CourseTable.get_children())
        for row in rows:
            self.CourseTable.insert('',END,values=row)
    
    def clear(self):
        self.show()
        self.var_course.set("")
        self.var_duration.set("")
        self.var_charges.set("")
        self.var_search.set("")
        self.txt_description.delete('1.0',END)
        self.txt_courseName.config(state='normal')

    def get_data(self,ev):
        self.txt_courseName.config(state='readonly')
        r = self.CourseTable.focus()
        content = self.CourseTable.item(r)
        row = content["values"]
        self.var_course.set(row[1])
        self.var_duration.set(row[2])
        self.var_charges.set(row[3])
        self.txt_description.delete('1.0',END)
        self.txt_description.insert(END,row[4])

    def insert(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()

        course_name = self.var_course.get().strip()
        duration = self.var_duration.get().strip()
        charges = self.var_charges.get().strip()
        description = self.txt_description.get("1.0", END).strip()
        
        if not course_name or not duration or not charges or not description:
            messagebox.showerror("Error", "All fields are required. Please fill in every detail.", parent=self.root)
            return
        if not charges.isdigit():
            messagebox.showerror("Error", "Charges must be a valid numeric value.", parent=self.root)
            return
        else:
            cur.execute("select * from course where name=?", (self.var_course.get(),))
            row = cur.fetchone()
            if row != None:
                messagebox.showerror("Error","Course Name Already Present",parent=self.root)
            else:
                cur.execute("insert into course(name,duration,charge,description) values(?,?,?,?)",(
                    self.var_course.get(),
                    self.var_duration.get(),
                    self.var_charges.get(),
                    self.txt_description.get("1.0",END),
                ))
                con.commit()
                messagebox.showinfo("Success","Course Inserted SuccessFully",parent=self.root)
                self.show()
                self.clear()

    def show(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        cur.execute("select * from course")
        rows = cur.fetchall()
        self.CourseTable.delete(*self.CourseTable.get_children())
        for row in rows:
            self.CourseTable.insert('',END,values=row)


    def update(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        course_name = self.var_course.get().strip()
        duration = self.var_duration.get().strip()
        charges = self.var_charges.get().strip()
        description = self.txt_description.get("1.0", END).strip()
        
        if not course_name or not duration or not charges or not description:
            messagebox.showerror("Error", "All fields are required. Please fill in every detail.", parent=self.root)
            return
        if not charges.isdigit():
            messagebox.showerror("Error", "Charges must be a valid numeric value.", parent=self.root)
            return
        else:
            cur.execute("select * from course where name=?", (self.var_course.get(),))
            row = cur.fetchone()
            if row == None:
                messagebox.showerror("Error","Select Course From List",parent=self.root)
            else:
                cur.execute("update course set duration=?,charge=?,description=? where name=?",(
                    self.var_duration.get(),
                    self.var_charges.get(),
                    self.txt_description.get("1.0",END),
                    self.var_course.get(),
                ))
                con.commit()
                messagebox.showinfo("Success","Course Update SuccessFully",parent=self.root)
                self.show()
                self.clear()

    def delete(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        if self.var_course.get()=="":
            messagebox.showerror("Error","Course Name Should be Required",parent=self.root)
        else:
            cur.execute("select * from course where name=?", (self.var_course.get(),))
            row = cur.fetchone()
            if row == None:
                messagebox.showerror("Error","Please Select Course From The List First",parent=self.root)
            else:
                op = messagebox.askyesno("Confirm","Do You Really Want To Delete?",parent=self.root)
                if op==True:
                    cur.execute("delete from course where name=?",(self.var_course.get(),))
                    con.commit()
                    messagebox.showinfo("Delete","Course Deleted Successfully",parent=self.root)
                    self.clear()

if __name__ == "__main__" :
    root = Tk()
    obj = CourseClass(root)
    root.mainloop()