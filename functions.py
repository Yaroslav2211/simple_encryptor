from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import db
import encryptions
import os

def browse_input_file():
    file = filedialog.askopenfile(
        title="Select Input File",
        filetypes=[
            ("All Files", "*.*"),
            ("Text Files", "*.txt"),
            ("Document Files", "*.doc;*.docx"),
            ("PDF Files", "*.pdf")
        ],
        mode = "rb"
    )
    if file:
        return file

def browse_output_file(input_file=None):
    initial_dir = "~"
    if input_file:
        initial_dir = os.path.dirname(input_file_var.get()) if input_file_var.get() else ""
    file_path = filedialog.asksaveasfilename(
        title="Save Encrypted File As",
        defaultextension=".enc",
        initialdir=initial_dir,
        filetypes=[
            ("Encrypted Files", "*.age"),
        ]
        )
    if file:
        return file
    
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

