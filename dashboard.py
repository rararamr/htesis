import tkinter as tk
import customtkinter
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from customtkinter import *
from tkinter import filedialog, ttk
from tkinter import *
from PIL import ImageTk, Image
#from utils import common_function

def create_new_window2(parent):
    # Destroy the parent window
    parent.destroy()

    # Create a new instance of the main application window
    home = customtkinter.CTk()
    home.title('Dashboard')

    # Set the dimensions and position of the window
    form_width = 1000
    form_height = 600       
    screen_width = home.winfo_screenwidth()
    screen_height = home.winfo_screenheight()
    x = (screen_width / 2) - (form_width / 2)
    y = (screen_height / 2) - (form_height / 2)
    home.geometry('%dx%d+%d+%d' % (form_width, form_height, x, y))

    # Load and display an image
    img1 = Image.open('back.jpg')
    resized_img = img1.resize((form_width, form_height))
    img1 = ImageTk.PhotoImage(resized_img)
    l2 = customtkinter.CTkLabel(master=home, image=img1)
    l2.pack(fill=BOTH, expand=True)

    #side_frame = customtkinter.CTkFrame(master=l2, width=100, height=400, bg_color='#ffffff00')
    #side_frame.place(relx=0, rely=0.5, anchor=tk.W, relheight=1, relwidth=0.3)  # Adjusted anchor

    frame = customtkinter.CTkFrame(master=l2, width=900, height=460, corner_radius=15)
    frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    # Add a welcome label
    label = customtkinter.CTkLabel(master=frame, text="Welcome to the Dashboard!", font=('Century Gothic', 20))
    label.pack(pady=20)

    label2 = customtkinter.CTkLabel(master=home, text="Welcome to the Dashboard!", font=('Century Gothic', 20))
    label2.place(x=10, y=100)
    dataframe_placeholder = customtkinter.CTkLabel(master=frame, text="")
    dataframe_placeholder.pack(pady=20)

    def upload_csv():
        # Open file dialog to select a CSV file
        filepath = filedialog.askopenfilename(
            initialdir="/",
            title="Select a File",
            filetypes=(("CSV files", "*.csv"), ("all files", "*.*"))
        )
        if not filepath:
            return  # User canceled the selection

        # Read the selected CSV file into a DataFrame
        df = pd.read_csv(filepath)

        # Display the DataFrame in a Treeview
        display_df(df, frame)

    def display_df(df, frame):
        # Create a frame for the table
        table_frame = customtkinter.CTkFrame(frame)
        table_frame.pack(pady=20, padx=10, fill=tk.BOTH, expand=True)

        # Insert new column for row numbers
        df.insert(0, 'Row Number', range(1, len(df) + 1))

        # Create Treeview with scrollbars
        tree = ttk.Treeview(table_frame, height=10)
        tree["columns"] = list(df.columns)
        tree["show"] = "headings"  # Hide the default first empty column

        # Configure column headers
        for col in df.columns:
            tree.heading(col, text=col, anchor="center")
            tree.column(col, width=100, anchor="center")

        # Insert data into Treeview
        for index, row in df.iterrows():
            tree.insert("", tk.END, values=list(row), tags=('centered',))

        tree.tag_configure('centered', anchor='center')

        def toggle_table():
            if tree.winfo_ismapped():
                tree.pack_forget()  # Hide the Treeview
                view_button.configure(text="View CSV")
            else:
                tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)  # Show the Treeview
                view_button.configure(text="Hide CSV")

        # Create and configure scrollbars
        y_scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=tree.yview)
        x_scrollbar = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=tree.xview)
        tree.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)

        # Initially hide the Treeview
        tree.pack_forget()

        # Create the "View CSV" button
        view_button = tk.Button(master=frame, text="View CSV", command=toggle_table)
        view_button.pack(side=BOTTOM, pady=15)

        y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        #x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

    def logout():
        home.destroy()
        import loginpage
        loginpage.login() # this will show the login page

    logout_button = customtkinter.CTkButton(master=home, text="Logout", command=logout,fg_color="#2B2B2B", text_color="white", hover_color="#FF0000", width=120)
    logout_button.pack(side=tk.BOTTOM, pady=10)
    # Create the "Upload CSV" button
    upload_button = customtkinter.CTkButton(master=frame, text="Upload CSV", command=upload_csv)
    upload_button.pack(side=BOTTOM, pady=20)

    # Mainloop for the new window
    home.mainloop()