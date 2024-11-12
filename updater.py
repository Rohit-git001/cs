#Updater

from tkinter import *
from tkinter import messagebox
import customtkinter as ctk
import mysql.connector as c

db = c.connect(host="localhost", user="root", passwd="sql123", database="test")
cur = db.cursor()

entries = []
labels = []
get_uno_entry, uno_label = None, None

def updater_init(master):
    global entries, labels, get_uno_entry, uno_label
    entries = []
    labels = []
    get_uno_entry, uno_label = None, None

    createLabels(master)
    createEntries(master)
    createButtons(master)

def createEntries(master):
    global get_uno_entry
    for i in range(7):
        entries.append(ctk.CTkEntry(master))
        entries[i].grid(row=i+1, column=1)

    get_uno_entry = ctk.CTkEntry(master)
    get_uno_entry.grid(row=8, column=1)

def createLabels(master):
    global uno_label
    texts = ["Uno:", "Uname:", "Password:", "Matches:", "Wins:", "Losses:", "Ties:", "Streak:"]
    for i in range(8):
        labels.append(ctk.CTkLabel(master, text=texts[i]))
        labels[i].grid(row=i, column=0)

    uno_label = ctk.CTkLabel(master, text="")
    uno_label.grid(row=0, column=1)

def get_values():
    uno = get_uno_entry.get()
    cur.execute(f"select * from tictactoe where uno = {uno}")
    data = cur.fetchall()[0]

    uno_label.configure(text=data[0])
    print(uno_label.cget("text"))
    for i in range(7):
        entries[i].delete(0, ctk.END)
        entries[i].insert(0, data[i + 1])

def set_values():
    uno = uno_label.cget("text")
    q = f"update tictactoe set uname = '{entries[0].get()}', password = '{entries[1].get()}', matches = {entries[2].get()}, wins = {entries[3].get()},losses = {entries[4].get()}, ties = {entries[5].get()}, streak = {entries[6].get()} where uno = {uno};"
    cur.execute(q)
    db.commit()

def createButtons(master):
    get_button = ctk.CTkButton(master, text="Get", command=get_values)
    get_button.grid(row=8, column=0)

    set_button = ctk.CTkButton(master, text="Set", command=set_values)
    set_button.grid(row=9, column=1)

if __name__ == "__main__":
    root = ctk.CTk()
    updater_init(root)
    root.mainloop()