import tkinter as tk 
from tkinter import messagebox
from Temp_Ramping import MeerstetterTEC 
import logging 

# initialize controller
tec = MeerstetterTEC()

def updateCurrentTemp():
    current_temp = tec.get_data()["object temperature"][0]
    temperature_label.config(text=f"Current temperature: {current_temp}")
    root.after(1000, updateCurrentTemp)



def startRamp():
    try:
        starting_temp = float(starting_temp_entry.get())
        target_temp = float(target_temp_entry.get())
        ramp_rate = float(ramp_rate_entry.get())
        number_of_wells = float(number_of_wells_entry.get())
    except ValueError:
        messagebox.showerror("Invalid input", "Please enter a number for all fields")
        return 
    
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s:%(module)s:%(levelname)s:%(message)s")
    # get the values from DEFAULT_QUERIES
    print(tec.get_data())
    # yeet the values
    tec.start_ramp_temp(starting_temp, target_temp, ramp_rate, number_of_wells)


def showInfo(buttonClicked):
    if buttonClicked == "Starting Temperature":
        messagebox.showinfo("Info", "beepboopboobee.")
    if buttonClicked == "Target Temperature":
        messagebox.showinfo("Info", "boop.")
    if buttonClicked == "Ramp Rate":
        messagebox.showinfo("Info", "beep.")
    if buttonClicked == "Number of Wells":
        messagebox.showinfo("Info", "beepbeep.")
    


root = tk.Tk()
root.geometry("400x465")


bottom_frame = tk.Frame(root)
bottom_frame.pack(side='bottom', anchor='w')

temperature_label = tk.Label(bottom_frame, text="Current temperature: ")
temperature_label.pack(side='left')

frame = tk.Frame(root)
frame.pack()

tk.Button(frame, text="Starting Temperature (℃)", command=lambda: showInfo("Starting Temperature")).grid(row=2, pady=(20,5))
#tk.Label(frame, text = "Starting Temperature (℃)", bg="lightgray").grid(row=2, pady=(20,5))
starting_temp_entry = tk.Entry(frame, bg="lightblue")
starting_temp_entry.grid(row=3, column=0)

tk.Button(frame, text="Target Temperature (℃)", command=lambda: showInfo("Target Temperature")).grid(row=4, pady=(20,5))
#tk.Label(frame, text="Target Temperature (℃)", bg="lightgray").grid(row=4, pady=(20,5))
target_temp_entry = tk.Entry(frame, bg="lightblue")
target_temp_entry.grid(row=5, column=0)

tk.Button(frame, text="Ramp Rate (℃)", command=lambda: showInfo("Ramp Rate")).grid(row=6, pady=(10,5))
#tk.Label(frame, text="Ramp rate", bg="lightgray").grid(row=6, pady=(10, 5))
ramp_rate_entry = tk.Entry(frame, bg="lightblue")
ramp_rate_entry.grid(row=7, column=0)

tk.Button(frame, text="Number of Wells", command=lambda: showInfo("Number of Wells")).grid(row=8, pady=(10,5))
#tk.Label(frame, text="Number of Wells", bg="lightgray").grid(row=8, pady=(10, 5))
number_of_wells_entry = tk.Entry(frame, bg="lightblue")
number_of_wells_entry.grid(row=9, column=0)

tk.Button(frame, text="Start ramp", command=startRamp).grid(row=31, column=0, columnspan=2, pady=(10, 0))

updateCurrentTemp()

root.mainloop()
