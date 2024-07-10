from IPython.display import display, HTML

import xlwings as xw
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv
from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename
from data_fetch import *

Tk().withdraw() # We don't want a full GUI, so keep the root window from appearing
csv = askopenfilename() # show an "Open" dialog box and return the path to the selected file
print(csv)

# Load csv file from selection
csv_df = pd.read_csv(csv, sep=';')

print(csv_df.head())

time = csv_df["Time"]

print(time.head())