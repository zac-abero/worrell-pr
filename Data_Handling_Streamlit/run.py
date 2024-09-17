import streamlit
import streamlit_main

# Run this file to run the streamlit browser without needing to enter a new terminal message

import os 
os.system('streamlit run c:/Users/oppos/Desktop/worrell-pr/Data_Handling_Streamlit/streamlit_main.py')

'''
# Images
col1, col2 = st.columns(2, vertical_alignment='bottom')
# Plotting imagery
theo_img = os.path.abspath('Data_Handling_Streamlit/images/theo.png')
zac_img = os.path.abspath('Data_Handling_Streamlit/images/zacbike.png')
# Open the image from the specified path
theopng = Image.open(theo_img)
zacpng = Image.open(zac_img)

# adding image

with col1:
    st.image(theopng, caption='Theo exhausted after 35 miles and 5kft elevation', use_column_width=True)
with col2:
    st.image(zacpng, caption='Zac lifting bike after 35 miles and 5kft elevation', use_column_width=True)
'''
