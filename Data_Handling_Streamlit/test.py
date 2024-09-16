import streamlit as st
import pandas as pd
import process_data

# Locals
excel_fname = ""
csv_fname = ""
merged_csv = ""

data = ""

def merge_data_button():
    merged_csv = process_data.merge_data(excel_fname, csv_fname)
    st.download_button('Download CSV', merged_csv, 'merged_data.csv')
    
def display_data():
    df = pd.read_csv(data)
    st.dataframe(df)

st.write("Hello, welcome to the data processing app for the Worrell Lab Plate-Reader Project!")

excel_fname = st.file_uploader("Excel file")

csv_fname = st.file_uploader("CSV file")

data = st.file_uploader("CSV Data file")


st.button("Merge Data", on_click=merge_data_button)
st.button("Display Data", on_click=display_data)


# TODO: Alter the process_data.py code to merge files on time data - separate that and the cell analysis data so that they can be functional for graphing and manipulation of data
