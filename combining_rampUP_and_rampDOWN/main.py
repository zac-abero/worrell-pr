#custom modules
import TECGUI
import Temp_Ramping
import dataCollection
import tkinter as tk
from thread_manager import ThreadManager
#built-in modules
import threading

   
def main(): 
    # create a meerstetter TEC object
    MeerstetterTEC = Temp_Ramping.MeerstetterTEC()

    # Create synchronization events
    end_ramp_event = threading.Event()
    start_ramp_event = threading.Event()

    # init the GUI 
    root = tk.Tk()
    gui = TECGUI.GUI(root, MeerstetterTEC, end_ramp_event, start_ramp_event)

    # Initialize the ThreadManager
    thread_manager = ThreadManager()

    def check_start_event():
        if end_ramp_event.is_set():
            gui.root.after_cancel(check_start_event) #clear the queue
            gui.root.quit() #close the GUI
        elif start_ramp_event.is_set():
            # Continue with starting the threads after the start event is set (i.e. start button is clicked) 
            start_ramp_procedure(gui, MeerstetterTEC, end_ramp_event, thread_manager)
        else:
            # Check again after 100ms
            root.after(100, check_start_event)

    # Start polling for the event (to avoid blocking the main thread which is keeping the GUI responsive)
    root.after(100, check_start_event) 
    tk.mainloop()

def start_ramp_procedure(gui, MeerstetterTEC, end_ramp_event, thread_manager):
    # get ramp parameters
    starting_temp, target_temp, ramp_rate, numberOfWells, tec_output_file = gui.ramp_parameters    

    # create a data collection object and threads
    data = dataCollection.dataCollection(MeerstetterTEC)
    
    # Create threads using ThreadManager
    thread_manager.create_thread(data.writeToCSV, (end_ramp_event, tec_output_file))
    thread_manager.create_thread(MeerstetterTEC.ramp_temp, (starting_temp, target_temp, ramp_rate, numberOfWells, end_ramp_event))

    # Start all threads
    thread_manager.start_all()
    
    # Create temperature graph
    temperature_graph = data.graphTemp(data, gui.graph_frame)
    temperature_graph.run_animation()

    # Start polling for shutdown event
    gui.root.after(100, lambda: handle_shutdown(gui, end_ramp_event, thread_manager)) 
       
def handle_shutdown(gui, end_ramp_event, thread_manager): 
    """this function combines threads and GUI shutdown"""
    if end_ramp_event.is_set(): #this means that the user has closed the GUI or the ramp has finished
        thread_manager.terminate_all(end_ramp_event) #kill the threads
        gui.root.after_cancel(handle_shutdown) #clear the queue
        gui.kill_ramp(False) #don't show the pop-up message
        gui.root.quit() #close the GUI
    else:
        # Check again after 100ms
        if gui.root is not None:
            gui.root.after(100, lambda: handle_shutdown(gui, end_ramp_event, thread_manager))




if __name__ == "__main__":
    main()