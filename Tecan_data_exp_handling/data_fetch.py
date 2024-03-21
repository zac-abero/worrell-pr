# Imports section

import xlwings as xw
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from win32com.client import dynamic

# Function to locate a cell with a given value in the sheet

def find_cell(value, range, sheet_number):
    for cell in wb.sheets[sheet_number].range(range)[1:]:
       # print(cell.value)
        if cell.value == value:
            break
    return cell

# Fetching the active workbook (ideally the one booted by the Tecan i-control software)

wb = xw.books.active

# Locate range of data (sheets are inverse indexed, Sheet1 becomes the last sheet in the array)

print(wb.sheets[0].range("A1").value)

# Selecting the first column and printing every value in it
# for cell in wb.sheets[0].range('A:A')[1:]:
#     print(cell.value)
#     if cell.value == "End Time:":
#         break

print(find_cell("Mean", 'B:B', 0))

