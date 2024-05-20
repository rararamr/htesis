import tkinter as tk
from tkinter import messagebox
import connection  # Assuming this file handles your database connection
import mysql


conn = connection.conn
def create_new_window(parent):
    reg_win = tk.Toplevel(parent)
    reg_win.title("User Registration")
    reg_win.configure(bg='#3B7A57')
    form_width = 300
    form_height = 200
    screen_width = reg_win.winfo_screenwidth()
    screen_height = reg_win.winfo_screenheight()
    x = (screen_width/2) - (form_width/2)
    y = (screen_height/2) - (form_height/2)
    reg_win.geometry('%dx%d+%d+%d' % (form_width, form_height, x, y))


    # Registration Form Labels and Entries
    tk.Label(reg_win, text="Full Name:", bg='#3B7A57', fg='white').grid(row=0, column=0, sticky="w")
    entry_fullname = tk.Entry(reg_win, width=30)
    entry_fullname.grid(row=0, column=1)

    tk.Label(reg_win, text="Email:", bg='#3B7A57', fg='white').grid(row=1, column=0, sticky="w")
    entry_email = tk.Entry(reg_win, width=30)
    entry_email.grid(row=1, column=1)

    tk.Label(reg_win, text="Username:", bg='#3B7A57', fg='white').grid(row=2, column=0, sticky="w")
    entry_username = tk.Entry(reg_win, width=30)
    entry_username.grid(row=2, column=1)

    tk.Label(reg_win, text="Password:", bg='#3B7A57', fg='white').grid(row=3, column=0, sticky="w")
    entry_password = tk.Entry(reg_win, width=30, show="*")
    entry_password.grid(row=3, column=1)

    def register_user():
        fullname = entry_fullname.get()
        email = entry_email.get()
        username = entry_username.get()
        password = entry_password.get()

        # Basic input validation
        if not all([fullname, email, username, password]):
            messagebox.showinfo("Error", "Please fill in all fields.")
            return

        try:
            # Check connection outside the try block
            if not connection.conn.is_connected():
                messagebox.showerror("Error", "Database connection failed.")
                return

            # Database insertion
            cursor = connection.conn.cursor()
            sql_query = "INSERT INTO test_user_info (fullname, email, username, password) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql_query, (fullname, email, username, password))
            connection.conn.commit()  # Commit the changes

            messagebox.showinfo("Success", "Registration successful!")
            reg_win.destroy()  # Close registration window
            parent.deiconify()  # Show the login window again
        except mysql.connector.Error as err:  # Catch specific MySQL errors
            messagebox.showerror("Error", f"Registration failed: {err}")

    def go_back():
        reg_win.destroy()  # Close the registration window
        parent.deiconify()  # Show the login window again

    tk.Button(reg_win, text="Back", command=go_back, bg='#1C352D', fg='white').place(x=90, y=100, height=30)  # Add to the grid
    tk.Button(reg_win, text="Register", command=register_user, bg='#1C352D', fg='white').place(x=145, y=100, height=30)