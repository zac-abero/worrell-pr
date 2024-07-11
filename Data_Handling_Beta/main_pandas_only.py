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

for sheet in book:   
    print(sheet)
