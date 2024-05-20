import tkinter
from tkinter import *

import connection
def create_new_window(parent):
    new_win = Toplevel(parent)  # Create a top-level window
    # ... (Add widgets and layout to new_win) ...
conn = connection.conn
form = tkinter.Tk()
form.configure(bg='#3B7A57')
form_width = 430
form_height = 600
screen_width = form.winfo_screenwidth()
screen_height = form.winfo_screenheight()
x = (screen_width/2) - (form_width/2)
y = (screen_height/2) - (form_height/2)
form.geometry('%dx%d+%d+%d' % (form_width, form_height, x, y))
form.title('Registration')