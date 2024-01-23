import streamlit as st 
import google.generativeai as genai 
import os
from dotenv import load_dotenv
import PyPDF2 as pdf 

# Load environment variables
load_dotenv()

# configure gemini api
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

# Gemini pro response
def get_gemini_response(input):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input)
    return response.text

# Get input pdf file
def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    n_pages = len(reader.pages) 
    for page in range(n_pages):
        p = reader.pages[page]
        text = text + '\n' + str(p.extract_text())
    return text

#Streamlit application
st.set_page_config(page_title="Smart ATS - Utkarsh Gaikwad")
st.header("Smart ATS - Utkarsh Gaikwad")
st.text("Improve your resume with ATS")
jd = st.text_area("Paste the Job Description : ")
uploaded_file = st.file_uploader("Upload your Resume",type='pdf',help='Please upload Resume in pdf format')

submit = st.button("Analyze Resume")

if submit:
    if uploaded_file is not None:
        # Get the text from file
        text = input_pdf_text(uploaded_file)
        print(text)
        #Prompt Template
        input_prompt=f""" Hey Act Like a skilled or very experienced ATS(Application Tracking System)
                          with a deep understanding of tech field,software engineering,data science ,data analyst
                          and big data engineer. Your task is to evaluate the resume based on the given job description.
                          You must consider the job market is very competitive and you should provide 
                          best assistance for improving thr resumes. 
                          Assign the percentage Matching based on Job Description and Resume
                          Also show the missing keywords with high accuracy. Please go through Entire Resume and Job Description thorougly.
                            
                          Resume:{text}
                            
                          Job description:{jd}

                          I want the 3 outputs by comparing above Resume and Job Description :
                          1. Percentage match of Resume with Job Desription 
                          2. Missing Keywords in Resume in bullet points
                          3. Summary of the Resume in bullet points """
        
        # Gemini response
        response = get_gemini_response(input_prompt)
        st.subheader("The Response is : ")
        st.write(response)        
