import pandas as pd
import numpy as np
import csv
import time
import os

def gen_data():

    cwd = os.path.dirname(os.path.abspath(__file__))
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")



    field_names = ["Time","CH 1 Object Temperature","CH 1 Actual Output Current","CH 1 Actual Output Voltage"]
    start_time =  pd.to_datetime('10/2/2024 12:42:56 PM')
    end_time = pd.to_datetime('10/2/2024 3:46:36 PM')
    
    period = [5, 6]
    
    # TODO: create new csv file, write sample data in a range from the start time to the end time for testing purposes on excel output
    with open(desktop_path, 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(field_names)
                    for i in period:
                        
                        data = [i, 1, 2, 3]
                        writer.writerow(data)
                        time.sleep(1)  # Add a delay to avoid busy-waiting

    return

gen_data()