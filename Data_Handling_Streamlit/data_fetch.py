# Imports section

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime

# find_cell: Function to locate a cell with a given value in the sheet and returns the cell

    # value - What you're looking for, particularly if a cell has "End Time:" in it

    # range - Which column you're looking in, format in cell range such as 'A:A'

    # sheet_number - The sheet number (sheets are inverse indexed, Sheet1 becomes the last sheet in the array)

    # Example formatting use of this function : find_cell("Mean", 'B:B', 0)

#XLwings version, deprecated
def find_cell(value, range, sheet_number):
    wb = xw.books.active
    for cell in wb.sheets[sheet_number].range(range)[0:]:
        if value == cell.value:
            break
        if cell.row >= 200:
            print("No cells with " + value + " in " + range)
            break
    return wb.sheets[sheet_number].range((cell.row,cell.column)).get_address(False, False)

#TODO: update this function to be able to break out of an infinite loop if there is one

# Pandas Version, a mask of the large .where pandas dataframe function
def find_cell(name, sheet_number):
    return sheet_number.where(sheet_number==name).dropna(axis=0, how='all')