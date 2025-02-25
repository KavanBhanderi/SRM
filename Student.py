from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import sqlite3
from datetime import datetime
from tkcalendar import DateEntry
import tkinter as tk 

class StudentManagement:
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
        title = Label(self.root, text="Manage Student Details", font=("goudy old style", 20, "bold"), bg="#033054", fg="white").place(x=10, y=15, width=1180, height=35)

        self.var_rollno = StringVar()
        self.var_name = StringVar()
        self.var_email = StringVar()
        self.var_gender = StringVar()
        self.var_dob= StringVar()
        self.var_contact =StringVar()
        self.var_admission = StringVar()
        self.var_course =StringVar()
        self.var_state = StringVar()
        self.var_city = StringVar()
        self.var_pin = StringVar()
        
         # ===== Widgets =====
        
        lbl_rollno = Label(self.root, text="Roll No.", font=("goudy old style", 15, "bold"), bg="white").place(x=10, y=60)
        self.txt_roll = Entry(self.root, textvariable=self.var_rollno, font=("goudy old style", 15), bg="white",state="readonly")
        self.txt_roll.place(x=130, y=60, width=200)

        lbl_name = Label(self.root, text="Name", font=("goudy old style", 15, "bold"), bg="white").place(x=10, y=100)
        Entry(self.root, textvariable=self.var_name, font=("goudy old style", 15), bg="white").place(x=130, y=100, width=200)
       
        lbl_email = Label(self.root, text="Email", font=("goudy old style", 15, "bold"), bg="white").place(x=10, y=140)
        Entry(self.root, textvariable=self.var_email, font=("goudy old style", 15), bg="white").place(x=130, y=140, width=200)
       
        lbl_gender = Label(self.root, text="Gender", font=("goudy old style", 15, "bold"), bg="white").place(x=10, y=180)
        Entry(self.root, textvariable=self.var_email, font=("goudy old style", 15), bg="white").place(x=130, y=140, width=200)
        
        self.var_gender=ttk.Combobox(self.root, textvariable=self.var_gender, values=("Select Gender","Male","Female","Others"),font=("goudy old style", 15),state='readonly',justify=CENTER)
        self.var_gender.place(x=130, y=180, width=200)
        self.var_gender.current(0)

        lbl_state = Label(self.root, text="State", font=("goudy old style", 15, "bold"), bg="white").place(x=10, y=220)
        Entry(self.root, textvariable=self.var_state, font=("goudy old style", 15), bg="white").place(x=130, y=220, width=150)

        lbl_city = Label(self.root, text="City", font=("goudy old style", 15, "bold"), bg="white").place(x=290, y=220)
        Entry(self.root, textvariable=self.var_city, font=("goudy old style", 15), bg="white").place(x=340, y=220, width=150)

        lbl_pin = Label(self.root, text="Pin", font=("goudy old style", 15, "bold"), bg="white").place(x=500, y=220)
        Entry(self.root, textvariable=self.var_pin, font=("goudy old style", 15), bg="white").place(x=550, y=220, width=150)

        lbl_address = Label(self.root, text="Address", font=("goudy old style", 15, "bold"), bg="white").place(x=10, y=260)
        self.txt_address = Text(self.root, font=("goudy old style", 15), bg="white")
        self.txt_address.place(x=130, y=260, width=570, height=100)
        
        today = datetime.today().date()
        lbl_dob = Label(self.root, text="DOB", font=("goudy old style", 15, "bold"), bg="white").place(x=350, y=60)
        self.dob_entry = DateEntry(self.root, textvariable=self.var_dob, font=("goudy old style", 15), bg="white", date_pattern="yyyy-mm-dd")
        self.dob_entry.place(x=500, y=60, width=200)
        self.dob_entry.config(mindate=today)

        lbl_contact = Label(self.root, text="Contact", font=("goudy old style", 15, "bold"), bg="white").place(x=350, y=100)
        Entry(self.root, textvariable=self.var_contact, font=("goudy old style", 15), bg="white").place(x=500, y=100, width=200)
        
        lbl_admission = Label(self.root, text="Admission Date", font=("goudy old style", 15, "bold"), bg="white").place(x=350, y=140)
        Entry(self.root, textvariable=self.var_admission, font=("goudy old style", 15), bg="white").place(x=500, y=140, width=200)
       
        lbl_course = Label(self.root, text="Course", font=("goudy old style", 15, "bold"), bg="white").place(x=350, y=180)
        self.course_list=[]
        self.var_course=ttk.Combobox(self.root, textvariable=self.var_course, values=("Select Course",self.course_list),font=("goudy old style", 15),state='readonly',justify=CENTER)
        self.var_course.place(x=500, y=180, width=200)
        self.var_course.current(0)
        self.fetch_courses()

        # ===== Buttons =====

        self.btn_add=Button(self.root, text="Save", font=("goudy old style", 15, "bold"), bg="blue", fg="white", cursor="hand2",command=self.insert)
        self.btn_add.place(x=150,y=400,width=110,height=40)
        self.btn_update=Button(self.root, text="Update", font=("goudy old style", 15, "bold"), bg="green", fg="white", cursor="hand2",command=self.update)
        self.btn_update.place(x=270, y=400, width=110, height=40)
        self.btn_delete=Button(self.root, text="Delete", font=("goudy old style", 15, "bold"), bg="red", fg="white", cursor="hand2",command=self.delete)
        self.btn_delete.place(x=390, y=400, width=110, height=40)
        self.btn_clear=Button(self.root, text="Clear", font=("goudy old style", 15, "bold"), bg="gray", fg="white", cursor="hand2",command=self.clear)
        self.btn_clear.place(x=510, y=400, width=110, height=40)

         # ===== Search Panel =====

        self.var_search = StringVar()
        lbl_search_roll = Label(self.root,text="Roll No.",font=("goudy old styl",15,"bold"),bg="white").place(x=720,y=60)
        txt_search_roll = Entry(self.root,textvariable=self.var_search,font=("goudy old styl",15,"bold"),bg="white").place(x=820,y=60,width=210)
        btn_search = Button(self.root,text="Search",font=("goudy old styl",15,"bold"),bg="blue",fg="white",cursor="hand2",command=self.search).place(x=1070,y=60,width=120,height=28)

        # ===== Content =====

        self.C_Frame = Frame(self.root,relief=RIDGE)
        self.C_Frame.place(x=720,y=100,width=470,height=340)

        scrolly = Scrollbar(self.C_Frame,orient=VERTICAL)
        scrollx = Scrollbar(self.C_Frame,orient=HORIZONTAL)
        self.CourseTable = ttk.Treeview(self.C_Frame,columns=("roll","name","email","gender","dob","contact","admission","course","state","city","pin","address"),xscrollcommand=scrollx.set,yscrollcommand=scrolly.set)
        
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.CourseTable.xview)
        scrolly.config(command=self.CourseTable.yview)
        
        self.CourseTable.heading("roll",text="Roll No.")
        self.CourseTable.heading("name",text="Name")
        self.CourseTable.heading("email",text="Email")
        self.CourseTable.heading("gender",text="Gender")
        self.CourseTable.heading("dob",text="D.O.B")
        self.CourseTable.heading("contact",text="Contact")
        self.CourseTable.heading("admission",text="Admission")
        self.CourseTable.heading("course",text="Course")
        self.CourseTable.heading("state",text="State")
        self.CourseTable.heading("city",text="City")
        self.CourseTable.heading("pin",text="Pin")
        self.CourseTable.heading("address",text="Address")
        self.CourseTable["show"] = 'headings'
        self.CourseTable.column("roll",width=100)
        self.CourseTable.column("name",width=100)
        self.CourseTable.column("email",width=100)
        self.CourseTable.column("gender",width=100)
        self.CourseTable.column("dob",width=100)
        self.CourseTable.column("contact",width=100)
        self.CourseTable.column("admission",width=100)
        self.CourseTable.column("course",width=100)
        self.CourseTable.column("state",width=100)
        self.CourseTable.column("city",width=100)
        self.CourseTable.column("pin",width=100)
        self.CourseTable.column("address",width=200)
        self.CourseTable.pack(fill=BOTH, expand=1)
        self.CourseTable.bind("<ButtonRelease-1>",self.get_data)
        self.show()

    #========== CRUD FUNCTION ==========

    def search(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM student WHERE roll LIKE ?", ('%' + self.var_search.get().strip() + '%',))
        rows = cur.fetchall()
        self.CourseTable.delete(*self.CourseTable.get_children())
        if rows:
            for row in rows:
                self.CourseTable.insert('', END, values=row)
        else:
            messagebox.showinfo("No Results", "No record found for the entered roll number.", parent=self.root)
   

    def validate_dob(self, dob):
        """ Validate if the DOB is in the format yyyy-mm-dd """
        try:
            datetime.strptime(dob, "%Y-%m-%d")
            return True
        except ValueError:
            return False
    
    def clear(self):
        self.show()
        self.var_rollno.set("")
        self.var_name.set("")   
        self.var_email.set("")
        self.var_gender.set("Select Gender")
        self.var_dob.set("")
        self.var_contact.set("")
        self.var_admission.set("")
        self.var_course.set("Select Course")
        self.var_state.set("")
        self.var_city.set("")
        self.var_pin.set("")
        self.txt_address.delete('1.0',END)
        self.txt_roll.config(state="readonly")

    def get_data(self,ev):
        self.txt_roll.config(state="readonly")
        r = self.CourseTable.focus()
        content = self.CourseTable.item(r)
        row = content["values"]
        if not row:
            messagebox.showerror("Error", "No data found in the selected row.", parent=self.root)
            return
        self.var_rollno.set(row[0])
        self.var_name.set(row[1])
        self.var_email.set(row[2])
        self.var_gender.set(row[3])
        self.var_dob.set(row[4])
        self.var_contact.set(row[5])
        self.var_admission.set(row[6])
        self.var_course.set(row[7])
        self.var_state.set(row[8])
        self.var_city.set(row[9])
        self.var_pin.set(row[10])
        self.txt_address.delete('1.0',END)
        self.txt_address.insert(END,row[11])

    def fetch_courses(self):
        con = sqlite3.connect("rms.db")
        cur = con.cursor()
        cur.execute("SELECT name FROM course")
        rows = cur.fetchall() 
        self.course_list = [row[0] for row in rows]  
        self.var_course['values'] = self.course_list  #

    def validate_email(self, email):
        """Validates email using regex."""
        import re
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(pattern, email)
    
    def insert(self):
            con = sqlite3.connect(database="rms.db")
            cur = con.cursor()

            roll = self.var_rollno.get().strip()
            name = self.var_name.get().strip()
            email = self.var_email.get().strip()
            gender = self.var_gender.get().strip()
            dob = self.var_dob.get().strip()
            contact = self.var_contact.get().strip()
            admission = self.var_admission.get().strip()
            course = self.var_course.get().strip()
            state = self.var_state.get().strip()
            city = self.var_city.get().strip()
            pin = self.var_pin.get().strip()
            address = self.txt_address.get("1.0", END).strip()

            if not all([name, email, gender, dob, contact, admission, course, state, city, pin, address]):
                messagebox.showerror("Error", "All fields are required. Please fill in every detail.", parent=self.root)
                return
            if not contact.isdigit() or len(contact) != 10:
                messagebox.showerror("Error", "Contact number must be a valid 10-digit numeric value.", parent=self.root)
                return
            if not pin.isdigit() or len(pin) != 6:
                messagebox.showerror("Error", "PIN must be a valid 6-digit numeric value.", parent=self.root)
                return
            if not self.validate_email(email):
                messagebox.showerror("Error", "Invalid email format.", parent=self.root)
                return
            if gender not in ["Male", "Female", "Other"]:
                messagebox.showerror("Error", "Gender must be Male, Female, or Other.", parent=self.root)
                return
            if course == "Select Course" :
                messagebox.showerror("Error","Please Select Course",parent=self.root)
                return
            if not self.validate_dob(dob):
                messagebox.showerror("Error", "Invalid DOB format. Please use yyyy-mm-dd.", parent=self.root)
                return
            cur.execute("SELECT * FROM student WHERE roll=? OR email=?", (roll, email))
            row = cur.fetchone()
            if row is not None:
                messagebox.showerror("Error", "Roll number or Email already exists.", parent=self.root)
                return
            cur.execute("INSERT INTO student (name, email, gender, dob, contact, admission, course, state, city, pin, address) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (name, email, gender, dob, contact, admission, course, state, city, pin, address),
            )
            con.commit()
            messagebox.showinfo("Success", "Student record inserted successfully!", parent=self.root)
            self.show()
            self.clear()
        
    def show(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        cur.execute("select * from student")
        rows = cur.fetchall()
        self.CourseTable.delete(*self.CourseTable.get_children())
        for row in rows:
            self.CourseTable.insert('',END,values=row)

    def update(self):
            con = sqlite3.connect(database="rms.db")
            cur = con.cursor()

            roll = self.var_rollno.get().strip()
            name = self.var_name.get().strip()
            email = self.var_email.get().strip()
            gender = self.var_gender.get().strip()
            dob = self.var_dob.get().strip()
            contact = self.var_contact.get().strip()
            admission = self.var_admission.get().strip()
            course = self.var_course.get().strip()
            state = self.var_state.get().strip()
            city = self.var_city.get().strip()
            pin = self.var_pin.get().strip()
            address = self.txt_address.get("1.0", END).strip()

            if not all([name, email, gender, dob, contact, admission, course, state, city, pin, address]):
                messagebox.showerror("Error", "All fields are required. Please fill in every detail.", parent=self.root)
                return
            if not contact.isdigit() or len(contact) != 10:
                messagebox.showerror("Error", "Contact number must be a valid 10-digit numeric value.", parent=self.root)
                return
            if not pin.isdigit() or len(pin) != 6:
                messagebox.showerror("Error", "PIN must be a valid 6-digit numeric value.", parent=self.root)
                return
            if not self.validate_email(email):
                messagebox.showerror("Error", "Invalid email format.", parent=self.root)
                return
            if gender not in ["Male", "Female", "Other"]:
                messagebox.showerror("Error", "Gender must be Male, Female, or Other.", parent=self.root)
                return
            if course == "Select Course" :
                messagebox.showerror("Error","Please Select Course",parent=self.root)
                return
            if not self.validate_dob(dob):
                messagebox.showerror("Error", "Invalid DOB format. Please use yyyy-mm-dd.", parent=self.root)
                return
            cur.execute("SELECT * FROM student WHERE roll=? OR email=?", (roll, email))
            row = cur.fetchone()
            if row == None:
                messagebox.showerror("Error", "Select Roll No. From List", parent=self.root)
                return
            cur.execute("UPDATE student SET name=?,email=?,gender=?,dob=?,contact=?,admission=?,course=?,state=?,city=?,pin=?,address=? where roll=?",(
                self.var_name.get(),
                self.var_email.get(),
                self.var_gender.get(),
                self.var_dob.get(),
                self.var_contact.get(),
                self.var_admission.get(),
                self.var_course.get(),
                self.var_state.get(),
                self.var_city.get(),
                self.var_pin.get(),
                self.txt_address.get("1.0",END),
                self.var_rollno.get(),

            ))
            con.commit()
            messagebox.showinfo("Success", "Student record updated successfully!", parent=self.root)
            self.show()
            self.clear()

    def delete(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        if self.var_rollno.get()=="":
            messagebox.showerror("Error","Roll No. Should be Required",parent=self.root)
        else:
            cur.execute("select * from student where roll=?", (self.var_rollno.get(),))
            row = cur.fetchone()
            if row == None:
                messagebox.showerror("Error","Please Select Course From The List First",parent=self.root)
            else:
                op = messagebox.askyesno("Confirm","Do You Really Want To Delete?",parent=self.root)
                if op==True:
                    cur.execute("delete from student where roll=?",(self.var_rollno.get(),))
                    con.commit()
                    messagebox.showinfo("Delete","Course Deleted Successfully",parent=self.root)
                    self.clear()

if __name__ == "__main__" :
    root = Tk()
    obj = StudentManagement(root)
    root.mainloop()

