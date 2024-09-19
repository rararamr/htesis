import tkinter as tk
import customtkinter
import pandas as pd
from tkinter import *
from tkinter import messagebox
from customtkinter import *
from tkinter import filedialog, ttk
from PIL import ImageTk, Image, ImageEnhance
import matplotlib.pyplot as plt
import statistics, os

global_filepath = None  # Global variable to store the file path


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
    img1 = Image.open('back1.png').convert('RGB')
    resized_img = img1.resize((form_width, form_height), Image.Resampling.LANCZOS)
    enhancer = ImageEnhance.Brightness(resized_img)
    adjusted_img = enhancer.enhance(0.5)  # Lower the brightness a bit
    img1_tk = ImageTk.PhotoImage(adjusted_img)
    l2 = Label(home, image=img1_tk)
    l2.image = img1_tk
    #l2 = customtkinter.CTkLabel(master=home, image=img1)
    l2.pack(fill=BOTH, expand=True)

    frame = customtkinter.CTkFrame(master=l2, width=900, height=460, corner_radius=15)
    frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    # Add a welcome label
    label = customtkinter.CTkLabel(master=frame, text="Welcome to the Dashboard!", font=('Century Gothic', 20))
    label.pack(pady=20)

    label2 = customtkinter.CTkLabel(master=home, text="CONTROL PANEL", font=('Century Gothic', 30))
    label2.place(x=10, y=100)
    dataframe_placeholder = customtkinter.CTkLabel(master=frame, text="")
    dataframe_placeholder.pack(pady=20)
    
    def resize_image(event):
        # Get the new dimensions of the window
        new_width = event.width
        new_height = event.height

        # Avoid resizing below a certain size to prevent errors
        if new_width > 300 and new_height > 300:
            # Resize the original image to fit the new window size
            new_img = img1.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # Convert the resized image to a PhotoImage
            new_img_tk = ImageTk.PhotoImage(new_img)

            # Update the label with the new image
            l2.configure(image=new_img_tk)
            l2.image = new_img_tk  # Keep a reference to avoid garbage collection

    # Bind the resize event to the window
    home.bind("<Configure>", resize_image)

    
    def upload_csv():
        global global_filepath  # Declare the global variable
        # Open file dialog to select a CSV file
        filepath = filedialog.askopenfilename(
            initialdir="/",
            title="Select a File",
            filetypes=(("CSV files", "*.csv"), ("all files", "*.*"))
        )
        if not filepath:
            return  # User canceled the selection

        global_filepath = filepath  # Store the file path in the global variable

        # Read the selected CSV file into a DataFrame
        df = pd.read_csv(filepath)

        # Display the DataFrame in a Treeview
        display_df(df, frame)

    def display_df(df, master):
        table_frame = customtkinter.CTkFrame(master)
        table_frame.pack(pady=20, padx=10, fill=tk.BOTH, expand=True)  # Add padding and expand/fill

        # Insert new column before 'OrderID'
        df.insert(0, 'Row Number', range(1, len(df) + 1))
    
        global tree
        global y_scrollbar
        global x_scrollbar
        
        
        # Create Treeview with scrollbars
        tree = ttk.Treeview(table_frame, height=10)
        tree["columns"] = list(df.columns)
        tree["show"] = "headings" # Hide the default first empty column

        # Configure column headers
        for col in df.columns:
            tree.heading(col, text=col, anchor="center")
            tree.column(col, width=100, anchor="center")


        #max_width = max(df[col].astype(str).map(len)) + 5  
        #tree.column(col, width=max_width * 6)  # Adjust the multiplier (8) as needed
        #tree.column(col, width=100)  # Adjust width as needed



        # Insert data
        for index, row in df.iterrows():
            tree.insert("", tk.END, values=list(row), tags=('centered',))
            #tree.insert("", tk.END, values=list(row))

        tree.tag_configure('centered', anchor='center')
        # Create and configure scrollbars
        y_scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=tree.yview)
        x_scrollbar = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=tree.xview)
        tree.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)

        # Initially hide the Treeview
        #tree.pack_forget() 

        def toggle_table():

            if tree.winfo_ismapped():
                tree.pack_forget() # Hide the Treeview
                view_button.configure(text="View CSV")
            else:
                tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True) # Show the Treeview
                view_button.configure(text="Hide CSV")
    
            # Create the "View CSV" button
        view_button = tk.Button(master=home, text="View CSV", command=toggle_table)
        view_button.place(x=10, y=300)

        y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

    def analyze_ratings():
        if not global_filepath:
            messagebox.showinfo("Error", "No CSV file uploaded!")
            return

        # Load your CSV file containing the ratings
        df = pd.read_csv(global_filepath)

        # Assuming your ratings are in a column named "rating"
        ratings = df["rating_star"]

        # Calculate statistics
        mean_rating = statistics.mean(ratings)
        median_rating = statistics.median(ratings)
        try:
            mode_rating = statistics.mode(ratings)  # Get the mode
        except statistics.StatisticsError:
            mode_rating = "No mode"  # Handle the case with no unique mode  # Get the first mode if there are multiple
        variance = statistics.variance(ratings)
        std_dev = statistics.stdev(ratings)
        

        # Print the results
        result_text = (f"Mean Rating: {mean_rating}\n"
                       f"Median Rating: {median_rating}\n"
                       f"Mode Rating: {mode_rating}\n"
                       f"Variance: {variance}\n"
                       f"Standard Deviation: {std_dev}")

        messagebox.showinfo("Ratings Analysis", result_text)

        plt.hist(ratings, bins=20, edgecolor='black')  # Adjust bins as needed

        # Plot mean, median, mode
        plt.axvline(mean_rating, color='red', linestyle='dashed', linewidth=1)
        plt.axvline(median_rating, color='blue', linestyle='dashed', linewidth=1)
        if mode_rating != "No mode":
            plt.axvline(mode_rating, color='green', linestyle='dashed', linewidth=1)
        
        # Add text for mean, median, mode
        plt.text(mean_rating, plt.ylim()[1]*0.9, 'Mean', color='red', ha='center')
        plt.text(median_rating, plt.ylim()[1]*0.8, 'Median', color='blue', ha='center')
        if mode_rating != "No mode":
            plt.text(mode_rating, plt.ylim()[1]*0.7, 'Mode', color='green', ha='center')
        
        plt.xlabel('Rating Score')
        plt.ylabel('Frequency')
        plt.title('Distribution of Customer Ratings')
        plt.show()

    def remove_csv():
        global global_filepath
        global tree
        global y_scrollbar
        global x_scrollbar
        if global_filepath:
            try:
                # Delete the csv file
                os.remove(global_filepath)
                # Destroy table_frame and its children
                if tree:
                    tree.destroy()
                if y_scrollbar:
                    y_scrollbar.destroy()
                if x_scrollbar:
                    x_scrollbar.destroy()
                messagebox.showinfo("Success", "CSV file removed successfully!")
                global_filepath = None
            
            
            except FileNotFoundError:
                messagebox.showerror("Error", "File not found.")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while deleting: {e}")
        else:
            messagebox.showinfo("Info", "No CSV file to remove.")
    
    def settings():
        print('ily')
    
    def exit_program():
        home.quit()  # This will close the application
    
    # Create the "Upload CSV" button
    upload_button = customtkinter.CTkButton(master=home, text="Upload CSV", command=upload_csv)
    upload_button.place(x=10, y=250)

    #remove_button = customtkinter.CTkButton(master=frame, text="Remove CSV", command=lambda: remove_csv(frame))
    remove_button = customtkinter.CTkButton(master=home, text="Remove CSV", fg_color="#787276", command=remove_csv)  
    remove_button.place(x=10, y=350)
    # Create the "Analyze Ratings" button
    analyze_button = customtkinter.CTkButton(master=home, text="Analyze Ratings", fg_color="#FFD700", command=analyze_ratings)
    analyze_button.configure(text_color="black")
    analyze_button.place(x=10, y=400)

    exit_button = customtkinter.CTkButton(master=home, text="Exit", command=exit_program, fg_color="red", text_color="white", hover_color="#FF0000")
    exit_button.place(x=10, y=450)
    
    settings_button = customtkinter.CTkButton(master=home, text="Settings", command=settings, fg_color="green", text_color="white", hover_color="#FF0000")
    settings_button.place(x=10, y=500)
    # Mainloop for the new window
    home.mainloop()
