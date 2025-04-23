import tkinter as tk  # GUI Library
from tkinter import messagebox, ttk
import time

"""
This file contains a basic GUI for the temperature ramping software in the file Temp_Ramping.py.
It allows the user to input the starting temperature, target temperature, ramp rate, number of wells and output file name.
It also allows the user to start the ramp, pause the ramp, and end the program.
"""

class GUI:
    
    def __init__(self, root, tec, end_ramp_event, start_event) -> None:
        self.tec = tec
        self.root = root
        self.end_ramp_event = end_ramp_event
        self.start_event = start_event
        self.ramp_parameters = []
        self.setup_ui()
    
    def setup_ui(self, ):
        self.root.geometry("455x850")
        # Create and configure frames
        self.create_frames()
        # Set up the temperature label, buttons, and inputs
        self.create_Buttons()
        self.update_current_temp()
        self.create_inputs()
        
    def create_frames(self):
        self.input_frame = tk.Frame(self.root, width=200, height=300)
        self.progress_frame = tk.Frame(self.root)
        self.graph_frame = tk.Frame(self.root, width=900, height=500) #created but not yet displayed
        self.button_frame = tk.Frame(self.root)
        
        # Layout using grid
        self.input_frame.grid(row=0, column=0, rowspan=1, columnspan=1, sticky="nsew", padx=(30,20), pady=(25,20))
        self.progress_frame.grid(row=2, column=0, sticky="nw", padx=10, pady=10)
        self.button_frame.grid(row=1, column=0, padx=(30,20), pady=(10,0))
        self.root.grid_columnconfigure(1, weight=1)
        
    def create_Buttons(self):
        # Temperature label
        self.temperature_label = tk.Label(self.input_frame, text="Current temperature: ")
        self.temperature_label.grid(row=10, column=0, padx=(10,10), pady=(30,0), sticky="ew")
        
        # Buttons for ramp actions
        tk.Button(self.button_frame, text="Pause Ramp", command=self.pause_ramp).grid(row=0, column=0, padx=(5,5))
        tk.Button(self.button_frame, text="Start Ramp", command=self.get_start_ramp_parameters).grid(row=0, column=1, padx=(5,5))
        tk.Button(self.button_frame, text="End Program", command=lambda: self.kill_ramp(True)).grid(row=0, column=2, padx=(5,5)) 
        
    def create_inputs(self):        
        tk.Button(self.input_frame, text="Starting Temperature (℃)", command=lambda: self.showInfo("Begin_Temperature"), width=20).grid(row=0, column=0, pady=(0,20), sticky="ew")
        self.starting_temp_entry = tk.Entry(self.input_frame, bg="lightblue", width=40)
        self.starting_temp_entry.grid(row=1, column=0, sticky="ew")

        tk.Button(self.input_frame, text="End Temperature (℃)", command=lambda: self.showInfo("End_Temperature")).grid(row=2, column=0, pady=(50,20), sticky="ew")
        self.target_temp_entry = tk.Entry(self.input_frame, bg="lightblue")
        self.target_temp_entry.grid(row=3, column=0, sticky="ew")

        tk.Button(self.input_frame, text="Ramp Rate (℃)", command=lambda: self.showInfo("Ramp_Increment")).grid(row=4, column=0, pady=(50,20), sticky="ew")
        self.ramp_rate_entry = tk.Entry(self.input_frame, bg="lightblue")
        self.ramp_rate_entry.grid(row=5, column=0, sticky="ew")

        tk.Button(self.input_frame, text="Number of Wells", command=lambda: self.showInfo("Number_of_Wells")).grid(row=6, column=0, pady=(50,20), sticky="ew")
        self.number_of_wells_entry = tk.Entry(self.input_frame, bg="lightblue")
        self.number_of_wells_entry.grid(row=7, column=0, sticky="ew")
        
        tk.Button(self.input_frame, text="Output File Name", command=lambda: self.showInfo("Output_File_Name"), width=20).grid(row=8, column=0, pady=(50,20), sticky="ew")
        self.output_file_entry = tk.Entry(self.input_frame, bg="lightblue", width=40)
        self.output_file_entry.grid(row=9, column=0, sticky="ew")

        # Configure the grid to expand
        for i in range(0, 9):
            self.input_frame.grid_rowconfigure(i, weight=1)
   
    def showInfo(self, buttonClicked):
        if buttonClicked == "Begin_Temperature":
            messagebox.showinfo("Info", "This is the temperature you'd like to begin the ramp at.")
        if buttonClicked == "End_Temperature":
            messagebox.showinfo("Info", "This is the temperature you'd like to end the ramp at.")
        if buttonClicked == "Ramp_Increment":
            messagebox.showinfo("Info", "This is the temperature interval at which scans are initated. Smaller increments = more scans")
        if buttonClicked == "Number_of_Wells":
            messagebox.showinfo("Info", "This dictates how long the settle/pause time for a scan is. More Wells = More Time")
        if buttonClicked == "Output_File_Name":
            messagebox.showinfo("Info", "This is the name of the file that the TEC temperature data will be saved to")
    
    #TODO add progress bar function
    #def create_progress_bar(self):
    
    def update_current_temp(self):
        current_temp = self.tec.get_temp()
        self.temperature_label.config(text=f"Current temperature: {current_temp}")
        self.root.after(1000, self.update_current_temp)
    
    def get_start_ramp_parameters(self):
        try:
            starting_temp = float(self.starting_temp_entry.get())
            target_temp = float(self.target_temp_entry.get())
            ramp_rate = float(self.ramp_rate_entry.get())
            number_of_wells = float(self.number_of_wells_entry.get())
            TEC_output_file = self.output_file_entry.get()
            self.ramp_parameters = [starting_temp, target_temp, ramp_rate, number_of_wells, TEC_output_file]
            self.start_event.set()
            self.setup_graph()
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter a number for all fields")        
    
    def setup_graph(self):
        # Resize window to fit graph
        self.root.geometry("1800x900")  # Larger window to include the graph
        # Add the graph frame to the layout
        self.graph_frame.grid(row=0, column=1, rowspan=2, sticky="nsew", padx=(50,20), pady=(0,20))
    
    def check_start_event(self):
        if self.start_event.is_set():
            # Start the process since the event is set
            print(F'in if statement {self.start_event}')
            print("Start event triggered")
        else:
            # Continue checking after 100 ms
            print(F'in else statement {self.start_event}')
            self.root.after(100, self.check_start_event)
    
    def kill_ramp(self, show_popup=True):
        if show_popup:
            self.end_program_pop_up()
        self.tec.disable() #disable tec to stop temperature ramping
        self.end_ramp_event.set()
        self.root.after_cancel(self.update_current_temp) # Stop updating the temperature

    #pause ramp and adjacent helper functions
    def pause_ramp(self):
        held_temp = self.tec.get_temp()
        self.tec.set_temp(held_temp)
        
        new_window = tk.Tk()
        new_window.title= "Ramp Paused"
        
        new_window.geometry("350x100")
        
        # Create a label
        label = tk.Label(new_window, text="Do you want to continue your ramp?")
        label.pack(pady=10)
        
        #continue button
        continue_button = tk.Button(new_window, text="Continue", command=lambda: self.continue_ramp_helper(new_window, held_temp))
        continue_button.pack(side=tk.LEFT, padx=(10, 50), pady=10)
        
        #kill button
        kill_button = tk.Button(new_window, text="Kill", command=lambda: self.end_ramp_helper(new_window))
        kill_button.pack(side=tk.RIGHT, padx=(10, 50), pady=10)
    
    def end_ramp_helper(self, new_window):
        new_window.destroy()
        self.kill_ramp(True) 
        
    def continue_ramp_helper(self, new_window, held_temp):
        self.tec.start_ramp_temp(held_temp, self.ramp_parameters[1], self.ramp_parameters[2], self.ramp_parameters[3])
        new_window.destroy()
        
    @staticmethod
    def end_program_pop_up():
        # Show the initial message box
        messagebox.showinfo("Ramp Status", "Your ramp is over, shutting down system")
        
        # Create a new window for the progress bar
        progress_window = tk.Toplevel()
        progress_window.title("Shutting Down")
        
        # Add a progress bar to the window
        progress_bar = ttk.Progressbar(progress_window, orient="horizontal", length=300, mode="determinate")
        progress_bar.pack(pady=20)
        
        for i in range(101):
            progress_bar['value'] = i
            progress_window.update()
            time.sleep(0.03)  # 3 seconds / 100 steps = 0.03 seconds per step
    
        progress_window.destroy()  # Close the progress window