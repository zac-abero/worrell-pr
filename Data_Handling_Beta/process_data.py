from IPython.display import display, HTML

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv
import tkinter as tk 

from data_fetch import *
from tkinter.filedialog import askopenfilename
from openpyxl import * 

def chart(cell_name):

    # Variables

    # Establishing base dataframe for all read-in data to be placed into
    data = pd.DataFrame(columns = ['Sheet', 'StartTime', 'EndTime', 'Gain', 'Mean', 'StDev', 'Temperature'])    
    # Cell to investigate
    cell = cell_name

    # Open a selection screen for what sheet to run this function on

    tk.Tk().withdraw() # We don't want a full GUI, so keep the root window from appearing 
    workbook = askopenfilename() # show an "Open" dialog box and return the path to the selected file
    print(workbook + " successfully loaded")

    # Load excel workbook from selection
    book = pd.read_excel(workbook, None, header=None)

    tk.Tk().withdraw() # We don't want a full GUI, so keep the root window from appearing
    csv = askopenfilename() # show an "Open" dialog box and return the path to the selected file
    print(csv + " successfully loaded")

    # Load comma separated values file from selection with separator as ';'
    csv_df = pd.read_csv(csv, sep=';')
    csv_df.info()
    

    # Workbook stores sheets in nth to 1 order so we iterate through them with reveresed()
    for sheet in reversed(book):   
        
        # Prune workbook for empty sheets; i-control likes to create null sheets
        if book[sheet].empty: continue
        
        # Renaming workbook to not reference
        spreadsheet = book[sheet]
        
        # Create two dataframes
        # 1st dataframe is row delineated data such as start time, end time
        
        mode = find_cell("Mode", spreadsheet)
        gain = find_cell("Gain", spreadsheet)
        start_time = find_cell("Start Time:", spreadsheet)
        end_time = find_cell("End Time:", spreadsheet)     
        
        # List for all important named cell locations in the sheet
        value_list = [mode, gain, start_time, end_time]
        
        setup_df = pd.DataFrame()
        
        # This loop concatenates all the cell data
        for value in value_list:
            df2 = spreadsheet.loc[value.index].dropna(axis='columns', how='any')
            setup_df = pd.concat([setup_df, df2], axis=0)
        
        # Transpose and Correct Dataframe Labels
        setup_df = setup_df.T
        new_header = setup_df.iloc[0] # grab the first row for the header
        setup_df = setup_df[1:] # take the data less the header row
        setup_df.columns = new_header # set the header row as the df header
        setup_df.columns = setup_df.columns.str.strip() # stripping leading and trailing whitespace

        # Print Dataframe
        print(setup_df.head())
        
        # Check for valid indices before accessing the values
        start_time_index = setup_df["Start Time:"].first_valid_index()
        end_time_index = setup_df["End Time:"].first_valid_index()
        gain_index = setup_df["Gain"].first_valid_index()
        
        # Check if the column is in datetime format
        if not pd.api.types.is_datetime64_any_dtype(setup_df['Start Time:']):
            setup_df['Start Time:'] = pd.to_datetime(setup_df['Start Time:'], errors='coerce')

        if not pd.api.types.is_datetime64_any_dtype(setup_df['End Time:']):
            setup_df['End Time:'] = pd.to_datetime(setup_df['End Time:'], errors='coerce')

        if not pd.api.types.is_datetime64_any_dtype(csv_df['Time']):
            csv_df['Time'] = pd.to_datetime(csv_df['Time'], errors='coerce')

        
        try:
            if start_time_index is not None:
                start_time_value = setup_df['Start Time:'][start_time_index]
                start_time_value = pd.to_datetime(start_time_value)
            else:
                raise ValueError("No valid 'Start Time:' found")

            if end_time_index is not None:
                end_time_value = setup_df['End Time:'][end_time_index]
                end_time_value = pd.to_datetime(end_time_value)
            else:
                raise ValueError("No valid 'End Time:' found")

            if gain_index is not None:
                gain = setup_df['Gain'][gain_index]
            else:
                raise ValueError("No valid 'Gain' found") 
        except:
            pass
        
        
        csv_df['Time'] = pd.to_datetime(csv_df['Time'], format='mixed')
                
        temp_df = csv_df.loc[(csv_df['Time'] >= start_time_value) & (csv_df['Time'] <= start_time_value)]
        # print(temp_df.head())
        
        temperature = temp_df['CH 1 Object Temperature'].values[0] # drop name/dtypes from the merged data
        
        # 2nd dataframe will be the wells charted data with wells, mean, stdev
        
        well = find_cell("Well", spreadsheet)

        # Creating a dataframe for the table data in the excel sheet
        table_df = pd.DataFrame()
        
        # Selecting from the index of the "Well" cell until the end of the values attached to that table. Dropping all rows with invalid data.
        table_df = spreadsheet.iloc[well.index.item():-1].dropna(axis=0, how='any')
        new_header2 = table_df.iloc[0] #grab the first row for the header
        table_df = table_df[1:] #take the data less the header row
        table_df.columns = new_header2 #set the header row as the df header
        print(table_df.head(10))
        
        #mean = table_df.loc[table_df['Well'] == cell.upper()]['Mean'].values[0] # pairing on well type
        #st_dev = table_df.loc[table_df['Well'] == cell.upper()]['StDev'].values[0] # pairing on well type
        
        # Check if the DataFrame slice is empty
        mean_values = table_df.loc[table_df['Well'] == cell.upper()]['Mean']
        stdev_values = table_df.loc[table_df['Well'] == cell.upper()]['StDev']

        if mean_values.empty:
            raise ValueError(f"No data found for cell {cell.upper()} in 'Mean' column")
        else:
            mean = mean_values.values[0]

        if stdev_values.empty:
            raise ValueError(f"No data found for cell {cell.upper()} in 'StDev' column")
        else:
            st_dev = stdev_values.values[0]
        
        sheet_dict = {'Sheet': sheet, 'StartTime': start_time_value, 'EndTime' : end_time_value,  'Gain': gain, 'Temperature': temperature, 'Mean': mean, 'StDev': st_dev}
        
        df2 = pd.DataFrame([sheet_dict])

        data = data._append(df2, ignore_index = True)
        
        
    display(data)

    charted_data = data[["Temperature", "Mean"]].apply(pd.to_numeric, errors = 'coerce') # converts to numeric, leaves "INVALIDs" as NaN
    print(charted_data.head())
    plt.figure()

    charted_data.plot(x="Temperature", y="Mean")

    plt.show()
    