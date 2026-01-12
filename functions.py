from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import db
import encryptions

def fchoose(mode):
    if mode == "rb":
        return filedialog.askopenfile(mode=mode)
    if mode == "wb":
        return filedialog.asksaveasfile(mode=mode)
    
def encr_button_handler(users_listbox,con):
    ind = users_listbox.curselection()[0]
    username = users_listbox.get(ind)
    encryptions.encr(username,con)

def del_button_handler(users_listbox,con):
    ind = users_listbox.curselection()[0]
    username = users_listbox.get(ind)[0]
    db.del_user(con,username,"receivers")
    update_listbox(users_listbox,con,"receivers")

def update_listbox(users_listbox,con,table):
    users_listbox.delete(0,users_listbox.size())
    users = db.get_users(con, table)
    for x in range(0,len(users)):
        users_listbox.insert(x, users[x])
