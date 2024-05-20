import tkinter
from tkinter import *
from tkinter import Entry
from tkinter import messagebox
from mysql.connector import Error
import connection
import registration


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
form.title('User Login')

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
                messagebox.showinfo('Error',"Username and password is incorrect")
                return
            else:
                messagebox.showinfo('','Login successfully')
    except Error as e:
        messagebox.showinfo('.','Connection failed')
        
def open_new_window():
    registration.create_new_window(form)  # Call the function to create the window
    form.withdraw()  # Hide the login window



#labels
login_label = Label(form, text='Login', bg='#3B7A57', fg='#FFFFFF', font=('Arial', 35))

username_label = Label(form, text='Username:', bg='#3B7A57', fg='#FFFFFF', font=('Arial', 16))
txt_username = Entry(form, width=27, font=('Arial', 16))

password_label = Label(form, text='Password:', bg='#3B7A57', fg='#FFFFFF', font=('Arial', 16))
txt_password = Entry(form, width=27, show='*', font=('Arial', 16))

btn_login = Button(form, width=25, text='Login', font=('Arial', 15), command=check_login)
btn_login.configure(bg='#1C352D', fg='#FFFFFF')

label_signup = Label(form, text="Don't have an account?", bg='#3B7A57', 
                     fg="white", font=('Arial', 12))
btn_signup = Button(form, width=8, text="Sign Up", font=('Arial', 12), command=open_new_window)
btn_signup.configure(bg='#3B7A57', fg='#FFFFFF')

#placements
login_label.place(x=155, y=100, height=55)
username_label.place(x=50, y=245, height=35)
txt_username.place(x=50, y=280, height=35)
password_label.place(x=50, y=320, height=35)
txt_password.place(x=50, y=355, height=35)
label_signup.place(x=50, y=395, height=30)
btn_signup.place(x=215, y=395, height=30)
btn_login.place(x=70, y=430, height=35)
form.mainloop()