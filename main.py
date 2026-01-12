from tkinter import *
from tkinter import ttk
from functions import *
import db
import my_windows

con = db.connect()
root = Tk()
root.title("whatever")
root.geometry("400x100")
sendb = Button(root, text="Отправить", command= lambda: my_windows.encrypt_window(con))
sendb.pack(side="left", fill=Y)
recvb = Button(root, text="Принять", command= lambda: my_windows.decrypt_window(con))
recvb.pack(side="right", fill=Y)
root.mainloop()