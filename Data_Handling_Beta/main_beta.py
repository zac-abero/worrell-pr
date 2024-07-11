from IPython.display import display, HTML

import xlwings as xw
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv
from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename
from data_fetch import *

# Open a selection screen for what sheet to run this function on
Tk().withdraw() # We don't want a full GUI, so keep the root window from appearing
workbook = askopenfilename() # show an "Open" dialog box and return the path to the selected file
print(workbook + " successfully loaded")

# Load excel workbook from selection
wb = xw.Book(workbook)

Tk().withdraw() # We don't want a full GUI, so keep the root window from appearing
csv = askopenfilename() # show an "Open" dialog box and return the path to the selected file
print(csv + " successfully loaded")

# Load csv file from selection with separator as ';'
csv_df = pd.read_csv(csv, sep=';')
csv_df.info() 

#TODO: Add try/catch loop or other timeout for Sheet1, See PEGTMP Meredith/Zac File

# Counter for sheet index
num_sheets = 0

for sheet in wb.sheets:
    num_sheets += 1

# Establishing base dataframe for all read-in data
data = pd.DataFrame(columns = ['Sheet', 'StartTime', 'EndTime', 'Gain', 'Mean', 'StDev', 'Temperature'])

for sheet in wb.sheets:
    # Excel is 1-based 
    sheet_number = num_sheets - sheet.index
    
    startTime_position = find_cell("Start Time:", 'A:A', sheet_number)
    endTime_position = find_cell("End Time:", 'A:A', sheet_number)
    gain_position = find_cell("Gain", 'A:A',  sheet_number)
    mean_position = find_cell("Mean", 'B:B',  sheet_number)
    stDev_position = find_cell("StDev", 'C:C', sheet_number)
    
    print(startTime_position, endTime_position, gain_position, mean_position, stDev_position)
    
    # If the cell is found, then we can extract the data, otherwise skip
    if startTime_position is None:   
        continue
    
    # .offset(r,c)
    startTime = sheet.range(startTime_position).offset(0,1).value
    endTime = sheet.range(endTime_position).offset(0,1).value
    gain = sheet.range(gain_position).offset(0,4).value
    mean = sheet.range(mean_position).offset(1,0).end('down').value
    stDev = sheet.range(stDev_position).offset(1,0).end('down').value
    
    print(startTime, endTime)
    
    start_dt = pd.to_datetime(startTime)
    end_dt = pd.to_datetime(endTime)
    
    csv_df['Time'] = pd.to_datetime(csv_df['Time'])
            
    temp_df = csv_df.loc[(csv_df['Time'] >= start_dt) & (csv_df['Time'] <= end_dt)]
    print(start_dt, end_dt)
    print(temp_df.head())
        
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