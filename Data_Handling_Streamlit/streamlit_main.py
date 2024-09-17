import streamlit as st
import pandas as pd
import process_data
import matplotlib.pyplot as plt

# Locals
excel_fname = None
csv_fname = None
merged_csv = None


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
        df = pd.read_csv(data)
        fig, ax = plt.subplots()
        df.plot(ax=ax)
        st.pyplot(fig)
    else:
        st.error("Please upload a CSV data file.")

st.write("Hello, welcome to the data processing app for the Worrell Lab Plate-Reader Project!")

excel_fname = st.file_uploader("Excel file", type=['xlsx', 'xls'])
csv_fname = st.file_uploader("CSV file", type=['csv'])
data = st.file_uploader("CSV Data file", type=['csv'])

col1, col2 = st.columns(2)
with col1:
    st.button("Merge Data", on_click=merge_data_button)
    if merged_csv:
        st.download_button('Download CSV', merged_csv, 'merged_data.csv')

with col2:
    st.button("Display Data", on_click=display_data)
    
st.button("Display Graph", on_click=display_graph)


# TODO: Alter the process_data.py code to merge files on time data - separate that and the cell analysis data so that they can be functional for graphing and manipulation of data
