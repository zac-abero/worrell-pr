import pyautogui
import time
import tkinter

"""
This file contains the automate_GUI class which is used to automate the GUI of the Tecan software. 
It finds the location of the button that triggers the Tecan to scan and clicks it, so 
we can trigger the tecan to scan at the correct temperature intervals.
"""

class automate_GUI: 
        
    def __init__(self) -> None:
        self.final_mouse_x = 0
        self.final_mouse_y = 0
        self.user_confirmed = False
        
    #function that triggers the tecan to scan
    def scan(self, current_temp, hold_rate):
        print("allowing temp to stablize (holding temp for 1 min before scanning)")
        time.sleep(60)
        self.clickButton()
        print("holding & scanning @ " + str(current_temp))
        time.sleep(hold_rate)    
    
    def getButtonLocation(self, timeToWait):
        while not self.user_confirmed:
            
            # Give yourself a few seconds to navigate to the screen where the button is
            time.sleep(timeToWait)
            # Get the current position of the mouse (use this to find the button position)
            current_mouse_x, current_mouse_y = pyautogui.position()
            print(f"Current mouse position: {current_mouse_x}, {current_mouse_y}")
            self.popUpComfirmation(current_mouse_x, current_mouse_y)
    
    # Function to continue and close the window
    def on_continue(self, window,  current_mouse_x,  current_mouse_y ):
        self.final_mouse_x = current_mouse_x
        self.final_mouse_y = current_mouse_y
        self.user_confirmed = True
        window.destroy()

        
    # Function to rerun and close the window
    def on_rerun(self, window):
        window.destroy()
        automate_GUI.getButtonLocation(self, 5)

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
