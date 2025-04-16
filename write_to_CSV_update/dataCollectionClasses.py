import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import csv
import threading
import globals 
import datetime
import os

now = str(datetime.datetime.now())
now_no_spaces = now.replace(" ", "_")
now_corrected = now.replace(":", "-")

fname = (now_corrected + "_TEC_Temperature_output.csv")

def create_desktop_folder(foldername):
    folder_name = foldername

    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    folder_path = os.path.join(desktop_path, folder_name)

    try:
        os.mkdir(folder_path)
        print(f"Folder '{folder_name}' created on Desktop")
        return folder_path
    except FileExistsError:
        print(f"Folder '{folder_name}' already exists on Desktop.")
        return folder_path

class dataCollection:
    
    def __init__(self, MeerstetterTEC) -> None:
         self.tec = MeerstetterTEC
         self.data = None # store data in a list
         self.lock = threading.Lock()

    
    def getData(self):
        while not globals.kill_button_pressed:
            with self.lock:
                self.data = self.tec.get_data_csv() #issue is here
            time.sleep(1)  # Add a delay to avoid busy-waiting
    
    def writeToCSV(self):
                """    
                Writes data to a CSV file.

                This method opens a file named 'TEC_temperature_output.csv' and writes data to it in CSV format.
                The data is obtained using the `get_data_csv` method, and the field names for the CSV
                columns are specified in the `field_names` list.

                Returns: 
                None
                """
                
                field_names = ["Time","CH 1 Object Temperature","CH 1 Actual Output Current","CH 1 Actual Output Voltage"]
                
                csv_folder_name = "TEC_Output"
                
                create_desktop_folder(csv_folder_name)
                folder_path = create_desktop_folder(csv_folder_name)
                filepath = os.path.join(folder_path, fname)
                                
                with open(filepath, 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(field_names)
                    while not globals.kill_button_pressed:
                        with self.lock:
                            data = self.data
                        writer.writerow(data)
                        time.sleep(1)  # Add a delay to avoid busy-waiting
    
    def openThreadsDataCollection(self):
        #graph_temp_instance = self.graphTemp(self)
        
        data_thread = threading.Thread(target=self.getData)
        data_thread.daemon = True
        data_thread.start()

        csv_thread = threading.Thread(target=self.writeToCSV)
        csv_thread.daemon = True
        csv_thread.start()

        """ 
        temp_graph_thread = threading.Thread(target=graph_temp_instance.run_animation)
        temp_graph_thread.daemon = True
        temp_graph_thread.start()
        """
    
    class graphTemp:
        
        def __init__(self, parent_instance) -> None:
            self.parent = parent_instance
            # Initialize figure and axis
            self.fig, self.ax = plt.subplots()
            self.ax.grid(True)
            self.x_vals = []
            self.y_vals = []
            self.start_time = time.time()

    
            
        def animate(self, i): 
            current_time = time.time()
            elapsed_time = current_time - self.start_time   
            with self.parent.lock:      
                current_temp = self.parent.data[1]  #Access parent's data attribute
            
            self.x_vals.append(elapsed_time)
            self.y_vals.append(current_temp)
            
            self.ax.clear()
            self.ax.plot(self.x_vals, self.y_vals)
            
            plt.xlabel('Time (s)')
            plt.ylabel('Temperature (°C)')
            plt.title('Live Temperature Data')
        
        def run_animation(self):
            ani = animation.FuncAnimation(self.fig, self.animate, interval=2000)  # Update every 2000 milliseconds (1 second)
            plt.tight_layout()
            plt.show()
        
    
    