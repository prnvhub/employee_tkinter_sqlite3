import os
import tkinter
from tkinter import *
from tkinter import font
import sqlite3
import tkinter.messagebox as MessageBox
from tkinter import ttk
from ttkthemes import themed_tk as tk
from PIL import ImageTk,Image


t=tk.ThemedTk(theme='equilux')
t.geometry("750x800")
t.title("Employee Registration")
if "nt" == os.name:
    t.wm_iconbitmap(bitmap = "tie.ico")
else:
    t.wm_iconbitmap(bitmap = "@tie.xbm")

p=Image.open("bg.jpg")
p=p.resize((750,800))
p=ImageTk.PhotoImage(p)
pic=tkinter.Label(image=p)
pic.place(x=0,y=0)



lblname=Label(text='Name ',font=('bold',10),relief=RIDGE)
lblname.place(x=20,y=30)
e_nm=Entry()
e_nm.place(x=150,y=30)

lblage=Label(text='Age ',font=('bold',10),relief=RIDGE)
lblage.place(x=400,y=30)
e_age=Entry()
e_age.place(x=500,y=30)

lbldoj=Label(text='D.O.J ',font=('bold',10),relief=RIDGE)
lbldoj.place(x=20,y=70)
e_doj=Entry()
e_doj.place(x=150,y=70)

lblemail=Label(text='Email ',font=('bold',10),relief=RIDGE)
lblemail.place(x=400,y=70)
e_em=Entry()
e_em.place(x=500,y=70)

lblphone=Label(text='Phone ',font=('bold',10),relief=RIDGE)
lblphone.place(x=20,y=110)
e_ph=Entry()
e_ph.place(x=150,y=110)

genderlist=[
    "",
    "Male",
    "Female",
    "Others",
]
lblgender=Label(text="Gender",relief=RIDGE)
lblgender.place(x=400,y=110)
e_gr=ttk.Combobox(value=genderlist,width=19,state="readonly")
e_gr.place(x=500,y=110)

lbladdress=Label(text='Address ',font=('bold',10),relief=RIDGE)
lbladdress.place(x=20,y=150)
e_ad=Text()
e_ad.place(x=150,y=150,width=510,height=140)


def getData(event):
    selected_row = tv.focus()
    data = tv.item(selected_row)
    global row
    row = data["values"]
    e_nm.insert(0,row[1])
    e_age.insert(0,row[2])
    e_doj.insert(0,row[3])
    e_em.insert(0,row[4])
    e_ph.insert(0,row[5])
    e_gr.insert(0,row[6])
    e_ad.delete(1.0, END)
    e_ad.insert(END, row[7])


def add_employee():
    if (e_nm.get()=="" or e_age.get()=="" or e_doj.get()=="" or e_ph.get()=="" or e_ad.get("1.0",'end-1c')==""):
        MessageBox.showinfo('Insert Status','All fields are required')
    else:
        x=sqlite3.connect('employees1.db')
        cur=x.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS employees(id Integer Primary Key, name text, age text, doj text, email text, phone text, gender text, address text)""")
        cur.execute("INSERT INTO employees VALUES(NULL, :name, :age, :doj, :email, :phone, :gender, :address)",
                    {
                        'name':e_nm.get(),
                        'age':e_age.get(),
                        'doj':e_doj.get(),
                        'email':e_em.get(),
                        'phone':e_ph.get(),
                        'gender':e_gr.get(),
                        'address':e_ad.get("1.0",'end-1c')
                    })
        cur.execute("commit")
        MessageBox.showinfo('Insert Status','Inserted Successfully')
        x.close()
        clearAll()
        dispalyAll()


def update(id, name, age, doj, email, phone, gender, address):
    x=sqlite3.connect('employees1.db')
    cur=x.cursor()
    cur.execute(
        "update employees set name=?, age=?, doj=?, email=?, phone=?, gender=?, address=? where id=?",
        (name, age, doj, email, phone, gender, address, id))
    x.commit()
    x.close()


def update_employee():
    if (e_nm.get()=="" or e_age.get()=="" or e_doj.get()=="" or e_ph.get()=="" or e_ad.get("1.0",'end-1c')==""):
        MessageBox.showinfo('Insert Status','All fields are required')
    else:
        update(row[0],e_nm.get(), e_age.get(), e_doj.get(), e_em.get(), e_ph.get(), e_gr.get(),
              e_ad.get("1.0",'end-1c'))
        
        MessageBox.showinfo("Success", "Records Updated")
        clearAll()
        dispalyAll()




def fetch():
    x=sqlite3.connect('employees1.db')
    cur=x.cursor()
    cur.execute("SELECT * from employees")
    rows = cur.fetchall()
    x.commit()
    x.close()
    return rows

def dispalyAll():
    tv.delete(*tv.get_children())
    for row in fetch():
        tv.insert("", END, values=row)


def delete_employee():
    remove(row[0])
    MessageBox.showinfo("Success", "Records Deleted")
    clearAll()
    dispalyAll()


def remove(id):
    x=sqlite3.connect('employees1.db')
    cur=x.cursor()
    cur.execute("delete from employees where id=?", (id,))
    x.commit()
    x.close()


def clearAll():
    e_nm.delete(0,'end')
    e_age.delete(0,'end')
    e_doj.delete(0,'end')
    e_em.delete(0,'end')
    e_ph.delete(0,'end')
    e_gr.delete(0,'end')
    e_ad.delete("1.0",'end')


Button(text='Submit',command=add_employee,fg="white",bg="#097969", bd=0).place(x=190,y=320)
Button(text='Update',command=update_employee,fg="white", bg="#6495ED",bd=0).place(x=310,y=320)
Button(text='Delete',command=delete_employee,fg="white", bg="#880808",bd=0).place(x=430,y=320)
Button(text='Clear',command=clearAll,fg="black", bg="#EDEADE",bd=0).place(x=550,y=320)

# Table Frame
tree_frame = Frame(bg="#ecf0f1")
tree_frame.place(x=0, y=400, width=750, height=400)
style = ttk.Style()
style.configure("mystyle.Treeview", font=('Calibri', 8),
                rowheight=50)  # Modify the font of the body
style.configure("mystyle.Treeview.Heading", font=('Calibri', 10))  # Modify the font of the headings
tv = ttk.Treeview(tree_frame, columns=(1, 2, 3, 4, 5, 6, 7, 8), style="mystyle.Treeview")
tv.heading("1", text="ID")
tv.column("1", width=15)
tv.heading("2", text="Name")
tv.column("2", width=150)
tv.heading("3", text="Age")
tv.column("3", width=30)
tv.heading("4", text="D.O.J")
tv.column("4", width=80)
tv.heading("5", text="Email")
tv.column("5", width=150)
tv.heading("6", text="Phone")
tv.column("6", width=100)
tv.heading("7", text="Gender")
tv.column("7", width=50)
tv.heading("8", text="Address")
tv['show'] = 'headings'
tv.bind("<ButtonRelease-1>", getData)
tv.pack(fill=X)
dispalyAll()


t.mainloop()