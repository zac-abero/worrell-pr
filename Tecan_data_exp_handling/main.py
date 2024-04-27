import xlwings as xw
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from data_fetch import *

# Fetching the active workbook (ideally the one booted by the Tecan i-control software)

wb = xw.books.active

print(find_cell("Mean", 'B:B', 0))

#TODO: Create a dataframe that contains all critical information, StartTime, EndTime, Gain, Mean (Key, Value), StDev (Key, Value), Temperature (TEC .csv Import) 
#TODO: Add try/catch loop or other timeout for Sheet1, See PEGTMP Meredith/Zac File

for sheet in wb.sheets:
    df = pd.DataFrame()

    print(find_cell("Start Time:", 'A:A', sheet.index)) 
    print(sheet.index)

#TODO: Iterate sheets function, convert find_cell to exact cell location and then plug into iterate sheet
#TODO: continue until a graph of mean and temperature from the active data on meerstetter is achieved