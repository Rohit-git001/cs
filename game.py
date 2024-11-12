#Game

from tkinter import *
from tkinter import messagebox
import customtkinter as ctk
import mysql.connector as c

root = ctk.CTk()
db = c.connect(host="localhost", user="root", passwd="sql123", database="test")
cur = db.cursor()

game_window = ctk.CTkToplevel(root)
game_window.destroy()

players = ["X", "O"]
player = "X"
users = {}

board = [['','',''],['','',''],['','','']]
board_buttons = []

reset_button = None

def game_init(master):
    global board, board_buttons, users
    board = [['','',''],['','',''],['','','']]
    board_buttons = []
    users = {}

    game_get_users(ctk.CTkToplevel(master), "X")
    game_get_users(ctk.CTkToplevel(master), "O")

    game_createButtons(master)

def game_createButtons(master):
    for i in range(3):
        board_buttons.append([])
        for j in range(3):
            board_buttons[i].append(ctk.CTkButton(master, command=game_createCommand(i,j, master), text="", width=100, height=100, font=("Comic Sans MS", 50), 
                                    bg_color='cyan', fg_color="black"))
            board_buttons[i][j].grid(row=i, column=j)

    reset_button = ctk.CTkButton(master, height=100, font=ctk.CTkFont("Comic Sans MS", 50), bg_color="cyan", fg_color="black", command=game_reset, text="Reset")
    reset_button.grid(row=3, column=0, columnspan=3, sticky="EW")

def game_createCommand(i, j, master):
    def fun():
        global player, users

        if len(users.keys()) < 2:
            messagebox.showerror("Game error", "Users not entered")
            return 0

        if board[i][j] != '':
            messagebox.showwarning("Game error", "Already full")
            return 0
        
        board_buttons[i][j].configure(text=player)
        board[i][j] = player
        player = [i for i in players if i != player][0]

        state = game_checkBoard()
        if state == None:
            return 0
        elif state == 'Draw':
            unames = list(users.values())
            cur.execute(f"update tictactoe set matches = matches + 1, ties = ties + 1 where uname in ('{unames[0]}', '{unames[1]}')")
            db.commit()
            messagebox.showinfo("Game end", "Draw!")
            master.destroy()
        elif state in "XO":
            if state == "X":
                winner = users["X"]
                loser = users["O"]
            else:
                winner = users["O"]
                loser = users["X"]
            cur.execute(f"update tictactoe set matches = matches + 1, wins = wins + 1 where uname = '{winner}'")
            cur.execute(f"update tictactoe set matches = matches + 1, losses = losses + 1 where uname = '{loser}'")
            db.commit()
            messagebox.showinfo("Game end", f"{winner} wins!")
            master.destroy()

    return fun

def game_reset():
    for i in range(3):
        for j in range(3):
            board_buttons[i][j].configure(text='')
            board[i][j] = ''

def game_checkBoard():
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != '':
            return board[i][0]
        elif board[0][i] == board[1][i] == board[2][i] != '':
            return board[0][i]
    if board[0][0] == board[1][1] == board[2][2] != '':
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != '':
        return board[1][1]
    
    full = True
    for i in range(3):
        for j in range(3):
            if board[i][j] == '':
                full = False
                break
    if full:
        return "Draw"
    
    return None

def test(master):
    but = ctk.CTkButton(master, text="test", command=create_game_window)
    but.pack()

def create_game_window():
    global game_window
    if game_window.winfo_exists() == 0:
        game_window = ctk.CTkToplevel(root)
        game_init(game_window)

def game_get_users(master, player):
    user_input = ctk.CTkEntry(master)
    passwd_input = ctk.CTkEntry(master, show="*")

    but = ctk.CTkButton(master, text="Test", command=update_user(master, user_input, passwd_input, player))
    
    user_input.pack()
    passwd_input.pack()
    but.pack()

def update_user(master: ctk.CTk, user_input: ctk.CTkEntry, passwd_input: ctk.CTkEntry, player):
    def fun():
        user = user_input.get()
        passwd = passwd_input.get()
    
        cur.execute(f"select count(*) from tictactoe where uname = '{user}'")
        if cur.fetchall()[0][0] == 0:
            messagebox.showerror("UserError", "User does not exist")
            return 0
        
        cur.execute(f"select password from tictactoe where uname = '{user}'")
        if cur.fetchall()[0][0] == passwd:
            users[player] = user
            print(users)
            master.destroy()
        else:
            messagebox.showerror("UserError", "Incorrect Password")
    return fun

if __name__ == "__main__":
    root = ctk.CTk()
    test(root)
    root.mainloop()