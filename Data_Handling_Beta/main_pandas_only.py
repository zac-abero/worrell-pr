from IPython.display import display, HTML

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv
from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename
from openpyxl import *

# Open a selection screen for what sheet to run this function on

Tk().withdraw() # We don't want a full GUI, so keep the root window from appearing
workbook = askopenfilename() # show an "Open" dialog box and return the path to the selected file
print(workbook + " successfully loaded")

# Load excel workbook from selection
book = pd.read_excel(workbook, None)

Tk().withdraw() # We don't want a full GUI, so keep the root window from appearing
csv = askopenfilename() # show an "Open" dialog box and return the path to the selected file
print(csv + " successfully loaded")

# Load comma separated values file from selection with separator as ';'
csv_df = pd.read_csv(csv, sep=';')
csv_df.info()

# Establishing base dataframe for all read-in data
data = pd.DataFrame(columns = ['Sheet', 'StartTime', 'EndTime', 'Gain', 'Mean', 'StDev', 'Temperature'])

# Workbook stores sheets in nth to 1 order so we iterate through them with reveresed()
for sheet in reversed(book):   
    
    # Prune workbook for empty sheets; i-control likes to create null sheets
    if book[sheet].empty: continue
    
    start_time = book[sheet].loc
    print(start_time)
    
    
    
    # # Excel is 1-based 
    # sheet_number = len(book) - int(sheet)
    
    # # Find the cell position of the following strings
    # startTime_position = find_cell("Start Time:", 'A:A', sheet_number)
    # endTime_position = find_cell("End Time:", 'A:A', sheet_number)
    # gain_position = find_cell("Gain", 'A:A',  sheet_number)
    # mean_position = find_cell("Mean", 'B:B',  sheet_number)
    # stDev_position = find_cell("StDev", 'C:C', sheet_number)
    
    # # .offset(r,c)
    # startTime = sheet.range(startTime_position).offset(0,1).value
    # endTime = sheet.range(endTime_position).offset(0,1).value
    # gain = sheet.range(gain_position).offset(0,4).value
    # mean = sheet.range(mean_position).offset(1,0).end('down').value
    # stDev = sheet.range(stDev_position).offset(1,0).end('down').value