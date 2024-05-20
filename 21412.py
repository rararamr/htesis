import tkinter as tk

root = tk.Tk()

label = tk.Label(root, text="This is a label")
label.grid(row=0, column=0, sticky="nsew")  # Expand in all directions

button = tk.Button(root, text="Click Me")
button.grid(row=1, column=0, sticky="w")  # Stick to the left (west) side

root.grid_rowconfigure(0, weight=1)  # Row 0 expands when window is resized
root.grid_columnconfigure(0, weight=1)  # Column 0 expands when window is resized

root.mainloop()
