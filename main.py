from tkinter import *
from tkinter import ttk
from functions import *
from db import *
import my_windows

root = Tk()
root.title("whatever")
root.geometry("250x200")
but = Button(root, text="Отправить", command=my_windows.encrypt_window)
but.pack(anchor=W)
root.mainloop()