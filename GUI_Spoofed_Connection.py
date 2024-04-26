import tkinter as tk 
from tkinter import messagebox

class MockMeerstetterTEC:
    def get_data(self):
        return {"object_temperature": 25.0}

    def ramp_temp(self, target_temp, ramp_rate, hold_rate):
        print(f"Ramping temperature to {target_temp} at a rate of {ramp_rate} and holding for {hold_rate}")

tec = MockMeerstetterTEC()

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
        messagebox.showerror("Invalid input", "Please enter a number for all fields")
        return 
    
    tec.ramp_temp(target_temp, ramp_rate, hold_rate)


root = tk.Tk()
root.geometry("400x230")


bottom_frame = tk.Frame(root)
bottom_frame.pack(side='bottom', anchor='w')

temperature_label = tk.Label(bottom_frame, text="Current temperature: ")
temperature_label.pack(side='left')

frame = tk.Frame(root)
frame.pack()

tk.Label(frame, text="Target temperature (℃)", bg="lightgray").grid(row=2, pady=(20,5))
target_temp_entry = tk.Entry(frame, bg="lightblue")
target_temp_entry.grid(row=3, column=0)

tk.Label(frame, text="Ramp rate", bg="lightgray").grid(row=4, pady=(10, 5))
ramp_rate_entry = tk.Entry(frame, bg="lightblue")
ramp_rate_entry.grid(row=5, column=0)

tk.Label(frame, text="Hold rate", bg="lightgray").grid(row=7, pady=(10, 5))
hold_rate_entry = tk.Entry(frame, bg="lightblue")
hold_rate_entry.grid(row=8, column=0)

tk.Button(frame, text="Start ramp", command=startRamp).grid(row=11, column=0, columnspan=2, pady=(10, 0))

updateTemp()

root.mainloop()

"""root = tk.Tk()


temperature_label = tk.Label(root, text="Current temperature: ")
temperature_label.pack(side='bottom', anchor='w')

tk.Label(root, text="Target temperature (℃)").grid(row=2)
target_temp_entry = tk.Entry(root)
target_temp_entry.grid(row=3, column=0)

tk.Label(root, text="Ramp rate- the temperature interval you want to hold at").grid(row=4)
ramp_rate_entry = tk.Entry(root)
ramp_rate_entry.grid(row=5, column=0)

tk.Label(root, text="Hold rate- hold a temperature for any given time, measured in seconds").grid(row=7)
hold_rate_entry = tk.Entry(root)
hold_rate_entry.grid(row=8, column=0)

tk.Button(root, text="Start ramp", command=startRamp).grid(row=10, column=0, columnspan=2)

updateTemp()

root.mainloop()"""