import xlwings as xw
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from data_fetch import *

# Fetching the active workbook (ideally the one booted by the Tecan i-control software)

wb = xw.books.active

#TODO: Create a dataframe that contains all critical information, StartTime, EndTime, Gain, Mean (Key, Value), StDev (Key, Value), Temperature (TEC .csv Import) 
#TODO: Add try/catch loop or other timeout for Sheet1, See PEGTMP Meredith/Zac File

for sheet in wb.sheets:
    df = pd.DataFrame()
    
    # Excel is 1-based 
    sheet_number = sheet.index -1 
    
    startTime = find_cell("Start Time:", 'A:A', sheet_number)
    endTime = find_cell("End Time:", 'A:A', sheet_number)
    gain = find_cell("Gain", 'A:A',  sheet_number)
    mean = find_cell("Mean", 'B:B',  sheet_number)
    stDev = find_cell("StDev", 'C:C', sheet_number)
    # temp = find_cell("Temperature", 'B:B', sheet.index)
    
    print("Sheet " + str(sheet.index))
    print (startTime, endTime, gain, mean, stDev)

#TODO: Iterate sheets function, convert find_cell to exact cell location and then plug into iterate sheet
#TODO: continue until a graph of mean and temperature from the active data on meerstetter is achieved