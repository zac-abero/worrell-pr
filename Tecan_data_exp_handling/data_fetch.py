# Imports section

import xlwings as xw
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# find_cell: Function to locate a cell with a given value in the sheet and returns the cell

    # value - What you're looking for, particularly if a cell has "End Time:" in it

    # range - Which column you're looking in, format in cell range such as 'A:A'

    # sheet_number - The sheet number (sheets are inverse indexed, Sheet1 becomes the last sheet in the array)

    # Example formatting use of this function : find_cell("Mean", 'B:B', 0)

def find_cell(value, range, sheet_number):
    wb = xw.books.active
    for cell in wb.sheets[sheet_number].range(range)[0:]:
        if cell.value == value:
            break
        if cell.row >= 100:
            print("No cells with " + value + " in " + range)
            break
    return cell.row, cell.column


#TODO: update this function to be able to break out of an infinite loop if there is one

# def find_cell(value, range, sheet_number):
#     wb = xw.books.active
#     try:
#         for cell in wb.sheets[sheet_number].range(range)[0:]:
#             if cell.value == value:
#                 break
#     except:
#             if cell.row > 100:
#                 print("Value is out of range, skipping")
#     return cell.row, cell.column