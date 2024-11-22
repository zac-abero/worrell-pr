import streamlit as st
import pandas as pd
import process_data
import matplotlib.pyplot as plt
import os
import time
from PIL import Image

# Locals
excel_fname = None
csv_fname = None
merged_csv = None
cell = None


def merge_data_button():
    if excel_fname and csv_fname:
        merged_csv = process_data.merge_data(excel_fname, csv_fname)
        st.download_button('Download CSV', merged_csv, 'merged_data.csv')
    else:
        st.error("Please upload both Excel and CSV files.")

def display_data():
    if data:
        df = pd.read_csv(data)
        st.dataframe(df)
    else:
        st.error("Please upload a CSV data file.")
        
def display_graph():
    if data:
        df = pd.read_csv(data, header=0)    
        cell_list = df['Cell'].unique().tolist()
        cell = st.selectbox("Choose cell", cell_list) # radio updates for cells
        df = df[["Temperature", "Mean"]].loc[df['Cell'] == cell].apply(pd.to_numeric, errors = 'coerce') # converts to numeric, leaves "INVALIDs" as NaN
        st.dataframe(df)

        st.line_chart(df, x="Temperature", y="Mean", x_label="Temperature", y_label="Mean Fluorescence Intensity")
    else:
        st.error("Please upload a merged CSV data file.")
        
def display_cells():
    if data:
        df = pd.read_csv(data, header=0)    
        cell_list = df['Cell'].unique().tolist()
        cell = st.selectbox("Choose cell", cell_list)
        st.write("OING")
        
# Begin App Layout

# Header

st.header("Hello! welcome to the data processing app for the Worrell Lab Plate-Reader Project!")

# Sidebar
# st.sidebar.radio('Pages', options=['Merge Data', 'Data Analysis', 'Charting'])

# Logo
# Plotting imagery
logo_file = os.path.abspath('Data_Handling_Streamlit/images/worrell-lab.png')
slogo_file = os.path.abspath('Data_Handling_Streamlit/images/worrell-lab-small.png')

# Open the image from the specified path
logo = Image.open(logo_file)
logo_small = Image.open(logo_file)

# adding image
st.logo(logo, link='https://www.bradyworrell.com/',icon_image=logo_small)

# File Upload

excel_fname = st.file_uploader("Plate Reader Excel File", type=['xlsx', 'xls'])
csv_fname = st.file_uploader("TEC Controller Temperature CSV file", type=['csv'])
data = st.file_uploader("Merged CSV Data file", type=['csv'])
if data is not None:
    display_cells

col1, col2, col3 = st.columns(3, vertical_alignment="bottom")
with col1:
    st.button("Merge Data", on_click=merge_data_button)
    if merged_csv:
        st.download_button('Download CSV', merged_csv, 'merged_data.csv')

with col2:
    st.button("Display Data", on_click=display_data)
with col3:
    st.button("Display Graph", on_click=display_graph)
    

# TODO: Alter the process_data.py code to merge files on time data - separate that and the cell analysis data so that they can be functional for graphing and manipulation of data
