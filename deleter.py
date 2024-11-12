#Deleter

from tkinter import *
from tkinter import messagebox
import customtkinter as ctk
import mysql.connector as c

db = c.connect(host="localhost", user="root", passwd="sql123", database="test")
cur = db.cursor()
user_entry, passwd_entry = None, None

def deleter_init(master):
    createEntries(master)
    createButtons(master)

def createEntries(master):
    global user_entry, passwd_entry

    user_entry = ctk.CTkEntry(master)
    passwd_entry = ctk.CTkEntry(master, show="*")

    user_entry.pack()
    passwd_entry.pack()

def createDeletorQuery(master):
    def fun():
        user = user_entry.get()
        passwd = passwd_entry.get()
        cur.execute(f"select count(*) from tictactoe where uname = '{user}'")
        if cur.fetchone()[0] == 0:
            messagebox.showerror("DeleterError", "User does not exist")
            return 0
    
        cur.execute(f"select password from tictactoe where uname = '{user}'")
        if cur.fetchone()[0] == passwd:
            cur.execute(f"delete from tictactoe where uname = '{user}'")
            db.commit()
            master.destroy()
        else:  
            messagebox.showerror("DeleterError", "Incorrect password")
    
    return fun

def createButtons(master):
    but = ctk.CTkButton(master, text="Delete", command=createDeletorQuery(master))
    but.pack()

if __name__ == "__main__":
    root = ctk.CTk()
    deleter_init(root)
    root.mainloop()