import streamlit as st
import google.generativeai as genai
from PIL import Image
import os
import datetime as dt   


#Configure the model
key = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=key)
model = genai.GenerativeModel('gemini-2.5-flash-lite')


st.sidebar.title(':orange[UPLOAD YOUR IMAGE HERE]')
uploaded_image=st.sidebar.file_uploader('Here', type = ['jpeg', 'jpg', 'png'])
if uploaded_image :
    
    image = Image.open(uploaded_image)
    st.sidebar.subheader(':blue[UPLOADED IMAGE]')
    st.sidebar.image(image)


# Create main Page
st.title(':orange[STRUCTURAL DEFECTS--] :blue[AI assisted structured defect identifier in construction business]')
tips = '''To use the application , follow the steps given below{
1. Upload the image
2. Click on the button to generate summary
3. Click download to save the report generated'''
st.write(tips)
rep_title = st.text_input('Report Title :', None)
prep_by = st.text_input('Report Prepared By:', None)
prep_for = st.text_input('Report Prepared for:', None)

prompt = f'''Assume you are a structural engineer, the user has provided an image 
of a structure .You need to identify the structural defects in the image and generate 
a report and the report should contain as follows:

It should start with the title, prepared by and prepared for details. Provided by the user
user.
use {rep_title} as report title, {prep_by} as prepared by, {prep_for} as prepared for the same.
Also mention the current date from {dt.datetime.now().date()}


*Identify and classify the defect for e.g., crack, spelling ,corrosion, honeycombing etc.
*There could be more than 1 defect in the image. Identify all the defects seperately
*For each defect identified, provide a short description of the defect and its potential impact on
*For each measure the severity of the defect as low, medium or high
*Also mention if the defect is inevitable or avoidable
*Also mention the time before this defect needs to permanent structural failure
*Provide short term and long term solutions along with their estimated cost and estimated time
*What precautions and measures should be taken to avoid such defects in future
*How much percentage risk is involved in this defect
*The report generated should be in the word format
*Show the data in bullet points and tabular format wherever possible
*Make sure that the report does not exceeds 3 pages'''

if st.button('Generate Report'):
    if uploaded_image is None:
        st.error('Please upload an image first to generate the report')
    else:
        with st.spinner('Generating Report...'):
            response = model.generate_content([prompt,image], generation_config={'temperature':0.7, "top_k":0})
            st.write(response.text)


            st.download_button(
                   label='Download Report', 
                   data =response.text, 
                   file_name = 'structural_defect_report.txt',
                   mime = 'text/plain')

# Save the report to a text file
with open("structural_defect_report.txt", "w") as file:
            file.write(response.text)
        
        # Provide a download button for the report
with open("structural_defect_report.txt", "rb") as file:
            btn = st.download_button(
                label="DOWNLOAD REPORT",
                data=file,
                file_name="structural_defect_report.txt",
                mime="text/plain"
            )



