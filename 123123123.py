import tkinter
import customtkinter
from customtkinter import *
from PIL import ImageTk, Image

form = customtkinter.CTk()
#form.geometry('600x440')
form_width = 600
form_height = 440
screen_width = form.winfo_screenwidth()
screen_height = form.winfo_screenheight()
x = (screen_width/2) - (form_width/2)
y = (screen_height/2) - (form_height/2)
form.geometry('%dx%d+%d+%d' % (form_width, form_height, x, y))
form.title('User Login')
img1 = ImageTk.PhotoImage(Image.open('pic1.jpg'))
l1 = customtkinter.CTkLabel(master=form, image=img1)
l1.pack()
frame=customtkinter.CTkFrame (master=l1, width=320, height=360, corner_radius=15)
frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
form.mainloop()