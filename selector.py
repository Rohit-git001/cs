#Selector

from tkinter import *
from tkinter import messagebox
import customtkinter as ctk
import mysql.connector as c

db = c.connect(host="localhost", user="root", passwd="sql123", database="test")
cur = db.cursor()
orderby_dict = {"Name" : "uname", "Matches" : "matches", "Wins" : "wins", "Losses" : "losses", "Ties" : "ties", "Streak" : "streak"}
labels = []
orderby_val, ascdesc_val = None, None

data = []
page_label = None
pages = len(data)
page = 0

def selector_init(master):
    createMenu(master)
    createCheck(master)
    createButton(master)
    createLabels(master)

def createMenu(master):
    global orderby_val
    options = ["Name", "Matches", "Wins", "Losses", "Ties", "Streak"]
    orderby_val = StringVar()
    orderby_val.set("Name")

    menu = ctk.CTkOptionMenu(master, variable=orderby_val, values=options)
    menu.grid(row=0, column=1)

def createCheck(master):
    global ascdesc_val
    ascdesc_val = StringVar()
    ascdesc_val.set("asc")
    check = ctk.CTkCheckBox(master, variable=ascdesc_val, onvalue="desc", offvalue="asc", text="Descending")
    check.grid(row=0, column=2)

def createQuery():
    global data, pages, pages
    
    q = f"select * from userview order by {orderby_dict[orderby_val.get()]} {ascdesc_val.get()}"
    cur.execute(q)
    data = cur.fetchall()
    pages = len(data)
    page = 0

    for i in range(len(labels)):
        labels[i].configure(text=data[0][i])
    page_label.configure(text=f"Page: {page}")

def getPrevious():
    global page

    if not any(data):
        messagebox.showerror("SelectorError", "No data!!")
        return 0
    
    if page == 0:
        messagebox.showerror("SelectorError", "First Page!!")
        return 0
    
    page -= 1
    for i in range(len(labels)):
        labels[i].configure(text=data[page][i])
    page_label.configure(text=f"Page: {page}")

def getNext():
    global page

    if not any(data):
        messagebox.showerror("SelectorError", "No data!!")
        return 0
    
    if page == pages - 1:
        messagebox.showerror("SelectorError", "Last Page!!")
        return 0
    
    page += 1
    for i in range(len(labels)):
        labels[i].configure(text=data[page][i])
    page_label.configure(text=f"Page: {page}")

def createButton(master):
    query_but = ctk.CTkButton(master, text="Obtain", command=createQuery)
    query_but.grid(row=0, column=0)

    prev_but = ctk.CTkButton(master, text="Previous", command=getPrevious)
    prev_but.grid(row=8, column=0)

    next_but = ctk.CTkButton(master, text="Next", command=getNext)
    next_but.grid(row=8, column=2)

def createLabels(master):
    global page_label
    
    names = ["Uno", *orderby_dict.keys()]
    for i in range(len(names)):
        lbl = ctk.CTkLabel(master, text=names[i]+":")
        labels.append(ctk.CTkLabel(master, text=""))

        lbl.grid(row=i+1, column=0)
        labels[i].grid(row=i+1, column=1)

    page_label = ctk.CTkLabel(master, text="")
    page_label.grid(row=8, column=1)

if __name__ == "__main__":
    root = ctk.CTk()
    selector_init(root)
    root.mainloop()
