from tkinter import *
from tkinter import ttk
import db
from functions import *
import encryptions

def encrypt_window():
    encr_w = Tk()
    encr_w.title("Отправка")
    encr_w.geometry("400x200")
    con = db.connect()
    users_listbox = Listbox(encr_w)
    update_listbox(users_listbox,con,"receivers")
    encr_but = Button(encr_w,text="Зашифровать для получателя", command= lambda: encr_button_handler(users_listbox,con))
    encr_but.pack(anchor=NW)
    del_but = Button(encr_w,text="Удалить",command= lambda: del_button_handler(users_listbox,con))
    del_but.pack(anchor=NW,side="left")
    add_but = Button(encr_w,text="Добавить",command= lambda: create_user_window(users_listbox,con))
    add_but.pack(anchor=NE,side="right")
    users_listbox.pack(fill=X,padx=5, pady=5,side="bottom")

def create_user_window(users_listbox,con=db.connect()):
    add_w = Tk()
    add_w.title("Создание контакта")
    add_w.geometry("300x200")
    uname = Text(add_w,height=10, width=200)
    uname.pack(anchor=NW)
    pubkey = Text(add_w,height=10, width=200)
    pubkey.pack(anchor=SW)