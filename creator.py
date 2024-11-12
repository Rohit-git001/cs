#Creator

from tkinter import *
from tkinter import messagebox
import customtkinter as ctk
import mysql.connector as c

db = c.connect(host="localhost", user="root", passwd="sql123", database="test")
cur = db.cursor()

user_entry, passwd_entry = None, None

def creator_init(master):
    createEntries(master)
    createButtons(master)

def createEntries(master):
    global user_entry, passwd_entry
    
    user_entry = ctk.CTkEntry(master)
    passwd_entry = ctk.CTkEntry(master, show="*")

    user_entry.pack()
    passwd_entry.pack()

def getNextFree():
    cur.execute("select uno from tictactoe")
    nos = [i[0] for i in cur.fetchall()]
    i = 1
    while True:
        if i not in nos:
            break
        i += 1
    return i

def createCreatorQuery(master):
    def fun():
        user = user_entry.get()
        passwd = passwd_entry.get()
        cur.execute(f"select count(*) from tictactoe where uname = '{user}'")
        if cur.fetchone()[0] > 0:
            messagebox.showerror("CreatorError", "Username in use")
            return 0
        uno = getNextFree()
        cur.execute(f"insert into tictactoe values ({uno}, '{user}', '{passwd}', 0, 0, 0, 0, 0)")
        db.commit()
        master.destroy()

    return fun

def createButtons(master):
    but = ctk.CTkButton(master, text="Create", command=createCreatorQuery(master))
    but.pack()   

if __name__ == "__main__":
    root = ctk.CTk()
    creator_init(root)
    root.mainloop()