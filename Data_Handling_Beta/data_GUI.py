import tkinter as tk 
from tkinter import messagebox
import logging 
#import temperatureGraph

def cell_update():    
    print("cell...")
    # root.destroy()


def process_data():
    print("proccess data...")
    # root.destroy()


def showInfo(buttonClicked):
    if buttonClicked == "select_cell":
        messagebox.showinfo("Info", "This is the cell you would like to analyze")


root = tk.Tk()
root.geometry("200x200")

bottom_frame = tk.Frame(root)
bottom_frame.pack(side='bottom', anchor='w')

frame = tk.Frame(root)
frame.pack()

tk.Button(frame, text="Select Cell", command=lambda: showInfo("select_cell")).grid(row=2, pady=(20,5))
starting_temp_entry = tk.Entry(frame, bg="lightblue")
starting_temp_entry.grid(row=3, column=0)

# Create a new frame for the buttons
button_frame = tk.Frame(frame)
button_frame.grid(row=31, column=0, columnspan=3, pady=(10, 0))

# Place the buttons inside the button_frame
tk.Button(button_frame, text="Start", command=process_data()).pack(side=tk.LEFT, padx=5)

# Adjust the parent frame to center the button_frame
frame.columnconfigure(0, weight=1)

root.mainloop()
