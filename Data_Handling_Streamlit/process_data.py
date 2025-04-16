import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from data_fetch import *

# merge_data is a function that takes in two file paths (excel and csv) and merges the data based on time data

def merge_data(excel_path, csv_path):
    #print(excel_path)
    
    # Collect data into traversable format
    
    # Dictionary of Dataframes (Excel book with sheets)
    book = pd.read_excel(excel_path, None, header=None)

    # Dataframe of the CSV, python's onboard engine will be able to "sniff" the delimiter automatically.
    try:
        csv_df = pd.read_csv(csv_path, sep=None, engine="python")
    except:
        print("Delimiter is not available")
        
    # lowercasing column names to avoid potential naming issues
    csv_df.columns = csv_df.columns.str.lower()

    # Create a dataframe containing all desired data
    data = pd.DataFrame(columns = ['Sheet', 'Cell', 'StartTime', 'EndTime', 'Gain', 'Mean', 'StDev', 'Temperature'])   
    
     # Workbook stores sheets in nth to 1 order so we iterate through them with reveresed()
    for sheet in reversed(book):   
    
    # Prune workbook for empty sheets; i-control likes to create null sheets
        if book[sheet].empty: continue
    
        # Renaming workbook to not reference a gaudy variable
        spreadsheet = book[sheet]
        
        # Create two dataframes
        # 1st dataframe is row delineated data such as start time, end time
        
        gain = find_cell("Gain", spreadsheet)
        start_time = find_cell("Start Time:", spreadsheet)
        end_time = find_cell("End Time:", spreadsheet)     
        
        # List for all important named cell locations in the sheet
        value_list = [gain, start_time, end_time]
        
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
        
        # Check for valid indices before accessing the values
        start_time_index = setup_df["Start Time:"].first_valid_index()
        end_time_index = setup_df["End Time:"].first_valid_index()
        gain_index = setup_df["Gain"].first_valid_index()
        
        # Check if the column is in datetime format
        if not pd.api.types.is_datetime64_any_dtype(setup_df['Start Time:']):
            setup_df['Start Time:'] = pd.to_datetime(setup_df['Start Time:'], errors='coerce')

        if not pd.api.types.is_datetime64_any_dtype(setup_df['End Time:']):
            setup_df['End Time:'] = pd.to_datetime(setup_df['End Time:'], errors='coerce')

        if not pd.api.types.is_datetime64_any_dtype(csv_df['time']):
            csv_df['time'] = pd.to_datetime(csv_df['time'], errors='coerce')
        
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
        except Exception as e:
            print(f"An error occurred: {e}")
            raise
        
        
        csv_df['time'] = pd.to_datetime(csv_df['time'], format='mixed')
                
        temp_df = csv_df.loc[(csv_df['time'] >= start_time_value) & (csv_df['time'] <= start_time_value)]
        
        # Check if temp_df is empty before accessing its elements
        if temp_df.empty:
            raise ValueError("No data found in the specified time range")
        
        temperature = temp_df['ch 1 object temperature'].values[0] # drop name/dtypes from the merged data
        
       # 2nd dataframe will be the wells charted data with wells, mean, stdev

        well = find_cell("Well", spreadsheet)

        # Debugging statements
        print("Contents of spreadsheet:")
        print(spreadsheet)

        print("Value of well:")
        print(well)

        # Check if well.index.item() is within the bounds of the spreadsheet DataFrame
        if well.index.item() >= len(spreadsheet):
            raise IndexError(f"Index {well.index.item()} is out of bounds for spreadsheet with length {len(spreadsheet)}")

        # Creating a dataframe for the table data in the excel sheet
        well_table_df = pd.DataFrame()
        
        print("Index of well:")
        print(well.index)

        # Selecting from the index of the "Well" cell until the end of the values attached to that table. Dropping all rows with invalid data.
        well_table_df = spreadsheet.iloc[well.index.item():-1].dropna(axis=0, how='any')
        
        print(well_table_df)
        
        # Error handling
        if well_table_df.empty:
            raise ValueError("No data found in the well table")
        

        new_header2 = well_table_df.iloc[0]  # grab the first row for the header
        well_table_df = well_table_df[1:]  # take the data less the header row
        well_table_df.columns = new_header2  # set the header row as the df header
        
        # Creating values to add to the sheet
        cell = None
        mean = None
        st_dev = None
        
        for index, row in well_table_df.iterrows():
            cell = row['Well']
            mean = row['Mean']
            st_dev = row['StDev']
        
            sheet_dict = {'Sheet': sheet, 'Cell': cell, 'StartTime': start_time_value, 'EndTime' : end_time_value,  'Gain': gain, 'Temperature': temperature, 'Mean': mean, 'StDev': st_dev}
            df2 = pd.DataFrame([sheet_dict])
            data = data._append(df2, ignore_index = True)

    data_csv = data.to_csv(index=False, header = True, sep = ',', encoding = 'utf-8')            
    return(data_csv)