from tkinter import *
from tkinter import messagebox
import customtkinter as ctk
import mysql.connector as c

from game import game_init
from selector import selector_init
from deleter import deleter_init
from creator import creator_init
from updater import updater_init

db = c.connect(host="localhost", user="root", passwd="sql123", database="test")
cur = db.cursor()

window = None

windows = {}
funcs = {}

def startup(admin):
    window = ctk.CTk()
    face_init(window, admin)
    window.mainloop()

def is_admin (master):
    check_val = BooleanVar()
    check = ctk.CTkCheckBox(master, onvalue=True, offvalue=False, variable=check_val)
    check.pack()

    s = StringVar()
    passwd_entry = ctk.CTkEntry(master, textvariable=s)
    passwd_entry.pack()

    def check_admin ():
        cur.execute("select * from admin")
        s = passwd_entry.get()
        master.destroy()
        admin = check_val.get() and cur.fetchall()[0][0] == s
        startup(admin)

    cont_but = ctk.CTkButton(master, text="Continue", command=check_admin)
    cont_but.pack()

def opener(name, master):
    def func():
        if windows[name].winfo_exists():
            messagebox.showerror("FaceError", "Window open!")
            return 0
        windows[name] = ctk.CTkToplevel(master)
        funcs[name](windows[name])

    return func

def face_init (master, admin):
    global windows, funcs

    windows = {"Game": ctk.CTkToplevel(master), "Selector": ctk.CTkToplevel(master), "Deleter": ctk.CTkToplevel(master), "Creator": ctk.CTkToplevel(master)}
    funcs = {"Game": game_init, "Selector": selector_init, "Deleter": deleter_init, "Creator": creator_init}
    buttons = {}

    if admin:
        windows["Updater"] = ctk.CTkToplevel(master)
        funcs["Updater"] = updater_init
    
    for i in windows:
        windows[i].destroy()

    for i in windows:
        buttons[i] = ctk.CTkButton(master, text=i, command=opener(i, master))
        buttons[i].pack()

if __name__ == "__main__":
    root = ctk.CTk()
    is_admin(root)
    root.mainloop()
