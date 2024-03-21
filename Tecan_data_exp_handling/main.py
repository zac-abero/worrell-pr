import xlwings as xw
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from data_fetch import *

# Fetching the active workbook (ideally the one booted by the Tecan i-control software)

wb = xw.books.active

print(find_cell("Mean", 'B:B', 0))

#TODO: Iterate sheets function, convert find_cell to exact cell location and then plug into iterate sheet
#TODO: continue until a graph of mean and temperature from the active data on meerstetter is achieved