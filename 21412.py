import tkinter as tk

root = tk.Tk()
root.geometry("400x300")

label1 = tk.Label(root, text="Absolute (x, y)")
label1.place(x=50, y=50)

label2 = tk.Label(root, text="Relative (relx, rely)")
label2.place(relx=0, rely=0.5)  

label3 = tk.Label(root, text="Anchor NW")
label3.place(x=200, y=150, anchor="e")

button = tk.Button(root, text="Centered Button")
button.place(relx=0.5, rely=0.5, anchor="center", width=120, height=40)

root.mainloop()