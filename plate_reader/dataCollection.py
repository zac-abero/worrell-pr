import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import csv
import threading
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class dataCollection:
    
    def __init__(self, MeerstetterTEC) -> None:
        self.tec = MeerstetterTEC
        self.data_lock = threading.Lock()
        self.data = None

    def writeToCSV(self, end_ramp_event, tec_output_file):

        """    
        --fetches data and then writes a CSV file--
        This method opens a file with name specified by the user and writes data to it in CSV format.
        The data is fetched from the TEC controller and written to the file every second.
        The method runs until the end_ramp_event is set.
        """
        
        field_names = ["time", "object temperature", "output current", "output voltage"]
        fname = (tec_output_file + ".csv")
        
        with open(fname, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(field_names)
            while not end_ramp_event.is_set():
                print(f'end_ramp_event: {end_ramp_event.is_set()}')
                with self.data_lock:
                    self.data = self.tec.get_data_csv() 
                    writer.writerow(self.data)
                time.sleep(1)  # Write data to CSV file every 1 second
                print("write to csv running")
                print(f'data: {self.data}')
                print(f'end_ramp_event 2: {end_ramp_event.is_set()}')
            print("write to csv stopped")

    class graphTemp:
        """
        --creates a live graph of temperature data--
        This class creates a live graph of the temperature data collected by the TEC controller.
        The x-axis of the graph represents time in seconds, and the y-axis represents temperature in degrees Celsius.
        The graph is updated every 2 seconds.
        It shares the data attribute with the parent class dataCollection.
        It is embedded into the GUI using the FigureCanvasTkAgg class, and is triggered to start when the start button is clicked.
        """
        
        def __init__(self, data_collection, parent_frame ) -> None:
            self.parent = data_collection
            self.parent_frame = parent_frame
            
            # Initialize figure and axis
            self.fig, self.ax = plt.subplots(figsize=(8, 5.5))
            self.ax.grid(True)
            self.x_vals = []
            self.y_vals = []
            self.graph_start_time = time.time()
           
            # Create a canvas to embed the figure into Tkinter
            self.canvas = FigureCanvasTkAgg(self.fig, master=self.parent_frame)
            self.canvas.draw()
            self.canvas.get_tk_widget().grid(row=0, column=1, rowspan=2, sticky="nsew", padx=10, pady=10)  # Right side, spanning both rows

        def animate(self, i):         
            current_time = time.time()
            elapsed_time = current_time - self.graph_start_time   
            with self.parent.data_lock:      
                current_temp = self.parent.data[1]  #Access parent's data attribute
            
            self.x_vals.append(elapsed_time)
            self.y_vals.append(current_temp)
            
            self.ax.clear()   
            self.ax.plot(self.x_vals, self.y_vals)
            
            plt.xlabel('Time (s)')
            plt.ylabel('Temperature (°C)')
            plt.title('Live Temperature Data')
        
        def run_animation(self):
            ani = animation.FuncAnimation(self.fig, self.animate, interval=2000, cache_frame_data=False)  # Update every 2000 milliseconds (2 seconds)
            self.canvas.draw()  # Redraw the canvas
            