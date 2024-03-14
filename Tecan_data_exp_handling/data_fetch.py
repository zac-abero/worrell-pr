# Imports section

import xlwings as xw
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from win32com.client import dynamic

# Test print

print("Worrell Plate Reader sample data test")

# Fetching active workbook 

wb = xw.books.active

# Locate range of data (sheets are inverse indexed, Sheet1 becomes the last sheet in the array)

print(wb.sheets[0].range("A1").value)

# Rows
for cell in wb.sheets[0].range('A:A')[1:]:
    print(cell.value)
    if cell.value == "End Time:":
        break
