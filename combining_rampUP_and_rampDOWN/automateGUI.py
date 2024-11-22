import pyautogui
import time
import tkinter
from tkinter import messagebox

"""
This file contains the automate_GUI class which is used to automate the GUI of the Tecan software. 
It finds the location of the button that triggers the Tecan to scan and clicks it so we can trigger the tecan to scan at the correct temperature intervals.
"""

#TODO: replace this class with direct serial communication to the Tecan
class automateGUI: 
        
    def __init__(self) -> None:
        self.final_mouse_x = 0
        self.final_mouse_y = 0
        self.user_confirmed = False
        
    def scan(self, current_temp, hold_rate, end_ramp_event):
        """This function triggers the Tecan to scan at the correct temperature intervals"""
        if not end_ramp_event.is_set():
            print("allowing temp to stablize (holding temp for 1 min before scanning)")
            time.sleep(60)
            self.clickButton()
            print("holding & scanning @ " + str(current_temp))
            time.sleep(hold_rate)    
    
    def getButtonLocation(self):
        """--This function gets the location of the button that triggers the Tecan to scan--
            It montiors mouse activity and if the mouse has not moved for 5 seconds, it will pop up a confirmation window"""
        self.popUpInstructions()
        last_time = time.time()
        mouse_location = pyautogui.position()
        
        while not self.user_confirmed:
            button_location = pyautogui.position()
            # If the mouse has moved, update the last time the mouse was moved
            if button_location != mouse_location:
                last_time = time.time()
                mouse_location = button_location
            # If the mouse has not moved for 5 seconds, end the loop
            if time.time() - last_time > 5:
                print("Mouse has not moved for 5 seconds")    
                self.popUpComfirmation(button_location[0], button_location[1])
            
    # Function to continue and close the window
    def on_continue(self, window,  current_mouse_x,  current_mouse_y ):
        self.final_mouse_x = current_mouse_x
        self.final_mouse_y = current_mouse_y
        self.user_confirmed = True
        window.destroy()

    # Function to rerun and close the window
    def on_rerun(self, window):
        window.destroy()
        self.getButtonLocation()

    def popUpInstructions(self):
        messagebox.showinfo("Instructions", "Navigate to the screen where the tecan's start button is located. Hover your mouse over the button until the confimation window appears. \n click 'ok' to continue.")
        
    def popUpComfirmation(self, current_mouse_x, current_mouse_y):
        # Create a window
        window =tkinter.Tk()
        window.title("Confirmation")
        
        #set window size
        window.geometry("350x100")
        
        # Create a label
        label = tkinter.Label(window, text="Meredith did you select the correct button?")
        label.pack(pady=10)
        
        #continue button
        continue_button = tkinter.Button(window, text="Continue", command=lambda: self.on_continue(window, current_mouse_x, current_mouse_y))
        continue_button.pack(side=tkinter.LEFT, padx=(10, 50), pady=10)
        
        #rerun button
        rerun_button = tkinter.Button(window, text="Rerun", command=lambda: self.on_rerun(window))
        rerun_button.pack(side=tkinter.RIGHT, padx=(10, 50), pady=10)
        
        window.mainloop()
        
    def clickButton(self):
    
        # Move the mouse to the button and click
        pyautogui.moveTo(self.final_mouse_x, self.final_mouse_y)
        pyautogui.click()

        print("Run button clicked")
