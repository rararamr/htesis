import tkinter
import customtkinter
from customtkinter import *
from tkinter import *
from tkinter import messagebox
from mysql.connector import Error
from PIL import ImageTk, Image
import connection
import registration
#import homepage
import homepage2
#from utils import common_function

conn = connection.conn

customtkinter.set_appearance_mode('system')
customtkinter.set_default_color_theme('green')

form = customtkinter.CTk()

form_width = 440
form_height = 600
screen_width = form.winfo_screenwidth()
screen_height = form.winfo_screenheight()
x = (screen_width/2) - (form_width/2)
y = (screen_height/2) - (form_height/2)
form.geometry('%dx%d+%d+%d' % (form_width, form_height, x, y))
#form.geometry('600x440')
form.title('User Login')
img1 = Image.open('pic1.jpg')
resized_img = img1.resize((form_width, form_height))
img1 = ImageTk.PhotoImage(resized_img)
#img1 = ImageTk.PhotoImage(Image.open('pic1.jpg'))
l1 = customtkinter.CTkLabel(master=form, image=img1)
l1.pack()
frame=customtkinter.CTkFrame (master=l1, width=320, height=360, corner_radius=15)
frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

def check_login():
    username = txt_username.get()
    password = txt_password.get()
    try:
        if conn.is_connected():
            pst = conn.cursor()
            sql_query = 'SELECT * FROM test_user_info WHERE username = %s AND password = %s'
            pst.execute(sql_query, (username, password))
            rs = pst.fetchone()
            if username == '' and password == '':
                messagebox.showinfo('Error',"Please enter username and password")
                return
            elif rs is None:
                messagebox.showinfo('Error',"Username and password is incorrect!")
                return
            else:
                messagebox.showinfo('','Login successful!')
                home_window()
    except Error as e:
        messagebox.showinfo('.','Connection failed')
def reg_window():
    registration.create_new_window(form)
    form.withdraw()
def home_window():
    homepage2.create_new_window2(form)
    form.destroy()

l2=customtkinter.CTkLabel(master=frame, text="Log into your Account",font=('Century Gothic',20))
l2.place(x=50, y=45)

txt_username = customtkinter.CTkEntry(master=frame, width=220, placeholder_text='Username')
txt_username.place(x=50, y=110)

txt_password = customtkinter.CTkEntry(master=frame, width=220, placeholder_text='Password', show="*")
txt_password.place(x=50, y=165)

button1 = customtkinter.CTkButton(master=frame, width=220, text="Login", command=check_login, corner_radius=6)
button1.place(x=50, y=240)

l3=customtkinter.CTkLabel(master=frame, text="Don't have an account?",font=('Century Gothic',12))
l3.place(x=50, y=205)

button2 = customtkinter.CTkButton(master=frame, width=5, text="Sign Up", command=reg_window, corner_radius=6, fg_color="#2B2B2B", text_color="white", hover_color="#106A43", font=('Century Gothic', 12))
button2.place(x = 195, y = 205)

form.mainloop()