from IPython.display import display, HTML

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv
from data_fetch import *
from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename
from openpyxl import *

# Open a selection screen for what sheet to run this function on

Tk().withdraw() # We don't want a full GUI, so keep the root window from appearing
workbook = askopenfilename() # show an "Open" dialog box and return the path to the selected file
print(workbook + " successfully loaded")

# Load excel workbook from selection
book = pd.read_excel(workbook, None, header=None)

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
    
    # Renaming workbook to not reference
    spreadsheet = book[sheet]
    
    # Find all important named cell locations in the sheet
    mode = find_cell("Mode", spreadsheet)
    gain = find_cell("Gain", spreadsheet)
    well = find_cell("Well", spreadsheet)
    start_time = find_cell("Start Time:", spreadsheet)
    end_time = find_cell("End Time:", spreadsheet) 
    
    value_list = [mode, gain, well, start_time, end_time]
    
    df1 = []
    
    for value in value_list:
        df1.append(spreadsheet.loc[value.index].dropna(axis=1))
    
    # How to find a cell
    # print(spreadsheet.loc[well.index, well.columns])
    
    # Create two dataframes
    # 1st dataframe is row delineated data such as start time, end time

    print(df1.head())
    
    # 2nd dataframe will be the wells charted data with wells, mean, stdev
    
    