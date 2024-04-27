import tkinter as tk 
from tkinter import messagebox
from example import MeerstetterTEC 

tec = MeerstetterTEC()

def updateTemp():
    currentTemp = tec.get_data()["object_temperature"]
    temperature_label.config(text=f"Current temperature: {currentTemp}")
    root.after(1000, updateTemp)

def startRamp():
    try:
        target_temp = float(target_temp_entry.get())
        ramp_rate = float(ramp_rate_entry.get())
        hold_rate = float(hold_rate_entry.get())
    except ValueError:
        message.showerror("Invalid input", "Please enter a number for all fields")
        return 
    
    tec.ramp_temp(target_temp, ramp_rate, hold_rate)

root = tk.Tk()

temperature_label = tk.Label(root, text="Current temperature: ")
temperature_label.grid(row=0, column=0, columnspan=2)

tk.Label(root, text="Target temperature (℃)").grid(row=1)
target_temp_entry = tk.Entry(root)
target_temp_entry.grid(row=1, column=1)

tk.Label(root, text="Ramp rate- the temperature interval you want to hold at").grid(row=2)
ramp_rate_entry = tk.Entry(root)
ramp_rate_entry.grid(row=2, column=1)

tk.Label(root, text="Hold rate- hold a temperature for any given time, measured in seconds").grid(row=3)
hold_rate_entry = tk.Entry(root)
hold_rate_entry.grid(row=3, column=1)

tk.Button(root, text="Start ramp", command=startRamp).grid(row=4, column=0, columnspan=2)

updateTemp()

root.mainloop()
