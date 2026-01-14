from tkinter import *
from tkinter import ttk
from functions import *
import db
import my_windows

con = db.connect()
my_windows.encrypt_window(con)