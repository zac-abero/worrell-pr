import tkinter as tk
from tkinter import ttk

class ExperimentGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("TEC and Tecan Experiment Control")
        # GUI components
        self.temperature_label = ttk.Label(root, text="Temperature:")
        self.temperature_entry = ttk.Entry(root)
        self.start_button = ttk.Button(root, text="Start Experiment", command=self.start_experiment)
        # Layout
        self.temperature_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        self.temperature_entry.grid(row=0, column=1, padx=10, pady=10)
        self.start_button.grid(row=1, column=0, columnspan=2, pady=20)
    def start_experiment(self):
        # Get temperature from the entry field
        temperature = self.temperature_entry.get()
        # TODO: Send temperature command to TEC control software
        # For demonstration purposes, print the command
        print(f"Setting TEC temperature to {temperature}°C")
        # TODO: Trigger Tecan data collection
        # For demonstration purposes, print a message
        print("Initiating Tecan data collection")
# Create the main application window
root = tk.Tk()
# Create an instance of the ExperimentGUI class
app = ExperimentGUI(root)
# Start the Tkinter event loop
root.mainloop()

# oingtest
# oingtestomega (









