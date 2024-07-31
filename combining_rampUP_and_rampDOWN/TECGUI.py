import tkinter as tk 
from tkinter import messagebox
from Temp_Ramping import MeerstetterTEC 
import logging 
import globals
#import temperatureGraph

"""
This file contains a basic GUI for the temperature ramping software in the file Temp_Ramping.py.
It allows the user to input the starting temperature, target temperature, ramp rate, and number of wells.
"""

# initialize controller
tec = MeerstetterTEC()
ramp_parameters = []

def updateCurrentTemp():
    current_temp = tec.get_temp()
    temperature_label.config(text=f"Current temperature: {current_temp}")
    root.after(1000, updateCurrentTemp)

def killRampAtRoot():
    globals.kill_button_pressed = True
    tec.disable()
    root.destroy()

def killRampPauseWindow(new_window):
    new_window.destroy()
    killRampAtRoot()
    
def continue_ramp(new_window):
    global ramp_parameters
    starting_temp, target_temp, ramp_rate, number_of_wells = ramp_parameters
    tec.start_ramp_temp(starting_temp, target_temp, ramp_rate, number_of_wells)
    new_window.destroy()


def pauseRamp():
    temp = tec.get_temp()
    tec.set_temp(temp)
    
    new_window = tk.Tk()
    new_window.title= "Ramp Paused"
    
    new_window.geometry("350x100")
    
    # Create a label
    label = tk.Label(new_window, text="Do you want to continue your ramp?")
    label.pack(pady=10)
    
    #continue button
    continue_button = tk.Button(new_window, text="Continue", command=lambda: continue_ramp(new_window))
    continue_button.pack(side=tk.LEFT, padx=(10, 50), pady=10)
    
    #kill button
    kill_button = tk.Button(new_window, text="Kill", command=lambda: killRampPauseWindow(new_window))
    kill_button.pack(side=tk.RIGHT, padx=(10, 50), pady=10)
    

def startRamp():
    global ramp_parameters
    
    try:
        starting_temp = float(starting_temp_entry.get())
        target_temp = float(target_temp_entry.get())
        ramp_rate = float(ramp_rate_entry.get())
        number_of_wells = float(number_of_wells_entry.get())
    except ValueError:
        messagebox.showerror("Invalid input", "Please enter a number for all fields")
        return 
    
    ramp_parameters = [starting_temp, target_temp, ramp_rate, number_of_wells]

    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s:%(module)s:%(levelname)s:%(message)s")
    # get the values from DEFAULT_QUERIES
    print(tec.get_data())
    # yeet the values
    # initialize temperature graph here (with threading)
    tec.start_ramp_temp(starting_temp, target_temp, ramp_rate, number_of_wells)


def showInfo(buttonClicked):
    if buttonClicked == "Begin Temperature":
        messagebox.showinfo("Info", "This is the initial temperature you'd like to begin with in the experiment.")
    if buttonClicked == "End Temperature":
        messagebox.showinfo("Info", "This is the final temperature you'd like to achieve in the experiment.")
    if buttonClicked == "Ramp Increment":
        messagebox.showinfo("Info", "This is the amount that each temperature ramps by")
    if buttonClicked == "Number of Wells":
        messagebox.showinfo("Info", "This dictates how long the settle/pause time for a scan is. More Wells = More Time")
    


root = tk.Tk()
root.geometry("400x570")

bottom_frame = tk.Frame(root)
bottom_frame.pack(side='bottom', anchor='w')

temperature_label = tk.Label(bottom_frame, text="Current temperature: ")
temperature_label.pack(side='left')

frame = tk.Frame(root)
frame.pack()

tk.Button(frame, text="Starting Temperature (℃)", command=lambda: showInfo("Begin Temperature")).grid(row=2, pady=(20,5))
#tk.Label(frame, text = "Starting Temperature (℃)", bg="lightgray").grid(row=2, pady=(20,5))
starting_temp_entry = tk.Entry(frame, bg="lightblue")
starting_temp_entry.grid(row=3, column=0)

tk.Button(frame, text="End Temperature (℃)", command=lambda: showInfo("End Temperature")).grid(row=4, pady=(20,5))
#tk.Label(frame, text="Target Temperature (℃)", bg="lightgray").grid(row=4, pady=(20,5))
target_temp_entry = tk.Entry(frame, bg="lightblue")
target_temp_entry.grid(row=5, column=0)

tk.Button(frame, text="Ramp Rate (℃)", command=lambda: showInfo("Ramp Increment")).grid(row=6, pady=(10,5))
#tk.Label(frame, text="Ramp rate", bg="lightgray").grid(row=6, pady=(10, 5))
ramp_rate_entry = tk.Entry(frame, bg="lightblue")
ramp_rate_entry.grid(row=7, column=0)

tk.Button(frame, text="Number of Wells", command=lambda: showInfo("Number of Wells")).grid(row=8, pady=(10,5))
#tk.Label(frame, text="Number of Wells", bg="lightgray").grid(row=8, pady=(10, 5))
number_of_wells_entry = tk.Entry(frame, bg="lightblue")
number_of_wells_entry.grid(row=9, column=0)

# Create a new frame for the buttons
button_frame = tk.Frame(frame)
button_frame.grid(row=31, column=0, columnspan=3, pady=(10, 0))

# Place the buttons inside the button_frame
tk.Button(button_frame, text="Pause Ramp", command=pauseRamp).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="Start Ramp", command=startRamp).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="Kill Ramp", command=killRampAtRoot).pack(side=tk.LEFT, padx=5)

# Adjust the parent frame to center the button_frame
frame.columnconfigure(0, weight=1)


updateCurrentTemp()

root.mainloop()
