import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename

# cd to FTIR folder and call "pyinstaller ftir_script.py" to generate an executable file

# Open a selection screen for what sheet to run this function on
Tk().withdraw() # We don't want a full GUI, so keep the root window from appearing
filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
print(filename)

# Load the data from excel
data = pd.DataFrame

# Read in the data from excel
data = pd.read_excel(filename, sheet_name=0)

# Display the data
data = data.iloc[0:1]

print(data)
