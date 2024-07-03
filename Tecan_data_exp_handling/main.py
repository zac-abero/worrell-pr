from IPython.display import display, HTML

import xlwings as xw
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from data_fetch import *

# need a file to be able to run auto-downloads on all necessary libraries used

# Fetching the active workbook (ideally the one booted by the Tecan i-control software)

wb = xw.books.active

#TODO: Create a dataframe that contains all critical information, StartTime, EndTime, Gain, Mean (Key, Value), StDev (Key, Value), Temperature (TEC .csv Import) 
#TODO: Add try/catch loop or other timeout for Sheet1, See PEGTMP Meredith/Zac File

num_sheets = 0

for sheet in wb.sheets:
    num_sheets += 1
    
data = pd.DataFrame(columns = ['Sheet', 'StartTime', 'EndTime', 'Gain', 'Mean', 'StDev', 'Temperature'])

for sheet in wb.sheets:
    # Excel is 1-based 
    sheet_number = num_sheets - sheet.index
    
    startTime_position = find_cell("Start Time:", 'A:A', sheet_number)
    endTime_position = find_cell("End Time:", 'A:A', sheet_number)
    gain_position = find_cell("Gain", 'A:A',  sheet_number)
    mean_position = find_cell("Mean", 'B:B',  sheet_number)
    stDev_position = find_cell("StDev", 'C:C', sheet_number)
    # figure out nonetype comparison in temperature or use starttime/endtime to calculate temp from .csv data
    ## temp = find_cell("Temperature", 'B:B', sheet_number)
    
    # need to create a dict for multiple data rows for mean and stdev and then append to the dataframe
    
    #   fluoresence vs temperature in real time
        
    startTime = sheet.range(startTime_position).offset(0,1).value
    endTime = sheet.range(endTime_position).offset(0,1).value
    gain = sheet.range(gain_position).offset(0,4).value
    mean = sheet.range(mean_position).offset(1,0).end('down').value
    stDev = sheet.range(stDev_position).offset(1,0).end('down').value
        
    sheet_dict = {'Sheet': sheet_number, 'StartTime': startTime, 'EndTime': endTime, 'Gain': gain, 'Mean': mean, 'StDev': stDev, 'Temperature': 0}
    
    df2 = pd.DataFrame([sheet_dict])

    data = data._append(df2, ignore_index = True)
    
display(data)

    
charted_data = data[["Gain", "Mean"]]

plt.figure()

charted_data.plot(x="Mean", y="Gain")

plt.show()

#TODO: Iterate sheets function, convert find_cell to exact cell location and then plug into iterate sheet
#TODO: continue until a graph of mean and temperature from the active data on meerstetter is achieved