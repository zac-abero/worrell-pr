import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time


class graphTemp:
        
        def __init__(self, meerstetter_instance) -> None:
            # Initialize figure and axis
            tec = meerstetter_instance
            fig, ax = plt.subplots()
            x_vals = []
            y_vals = []

        start_time = time.time()

        def get_temp(self):
            temp = self.tec.get_temp()
            return temp
            
        def animation(self): 
            current_time = time.time()
            elapsed_time = current_time - self.start_time
            current_temp = self.get_temp()
            
            self.x_vals.append(elapsed_time)
            self.y_vals.append(current_temp)
            
            self.ax.clear()
            self.ax.plot(self.x_vals, self.y_vals)
            
            plt.xlabel('Time (s)')
            plt.ylabel('Temperature (°C)')
            plt.title('Live Temperature Data')
        
        def run_animation(self):
            ani = animation.FuncAnimation(self.fig, animation(), interval=1000)  # Update every 1000 milliseconds (1 second)
            plt.tight_layout()
            plt.show()
        
