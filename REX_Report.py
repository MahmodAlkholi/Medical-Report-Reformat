

# import streamlit as st
# from PIL import Image
# import pytesseract
# import openai
# import fitz  # PyMuPDF

# with open('API.txt', 'r') as key:
#     data = key.read().strip()
# # Set your OpenAI API key
# openai.api_key = data

# # Streamlit App Layout
# st.title("Medical Report Reformatter")
# st.write("Upload an image or PDF of a medical report, and we will reformat it professionally as a pathology report.")

# # Initialize extracted text variables
# extracted_text_image = ""
# extracted_text_pdf = ""

# # Upload image
# uploaded_image = st.file_uploader("Upload an image...", type=["jpg", "jpeg", "png"])

# if uploaded_image is not None:
#     # Display the uploaded image
#     image = Image.open(uploaded_image)
#     st.image(image, caption="Uploaded Image", use_column_width=True)

#     # Extract text using Tesseract OCR
#     with st.spinner("Extracting text from the image..."):
#         extracted_text_image = pytesseract.image_to_string(image)

#     st.subheader("Extracted Text from Image")
#     st.write(extracted_text_image)

# # Upload PDF
# uploaded_pdf = st.file_uploader("Upload a PDF...", type=["pdf"])

# if uploaded_pdf is not None:
#     # Read PDF file from the uploaded file stream
#     with st.spinner("Extracting text from the PDF..."):
#         pdf_document = fitz.open(stream=uploaded_pdf.read(), filetype="pdf")
#         extracted_text_pdf = ""
        
#         # Extract text from all pages
#         for page in pdf_document:
#             extracted_text_pdf += page.get_text() + "\n"  # Append text from each page
        
#         pdf_document.close()

#     st.subheader("Extracted Text from PDF")
#     st.write(extracted_text_pdf)

# # Combine extracted text
# extracted_text = extracted_text_image + extracted_text_pdf

# if extracted_text:
#     # Define a prompt for GPT to rewrite the text as a pathology report
#     prompt = f"""
#     You are a professional pathology doctor. Below is a raw medical report extracted from an image or PDF.
#     Please reformat it into a structured pathology report with proper sections: Patient Details, 
#     Clinical History, Gross Description, Microscopic Examination, Diagnosis, Comments, 
#     Radiological Findings, Procedure, Recommendations, and Preliminary Pathology Remarks.

#     Raw Medical Report:
#     {extracted_text}
    
#     Rewritten Pathology Report:
#     """

#     if st.button("Generate Pathology Report"):
#         with st.spinner("Generating professional pathology report..."):
#             # OpenAI GPT API call to reformat the extracted text
#             response = openai.ChatCompletion.create(
#                 model="gpt-3.5-turbo",
#                 messages=[{"role": "user", "content": prompt}]
#             )
#             formatted_report = response.choices[0].message['content']

#         # Organize the generated report into sections
#         organized_report = formatted_report.replace("Patient Details:", "## Patient Details:\n") \
#                                             .replace("Clinical History:", "## Clinical History:\n") \
#                                             .replace("Gross Description:", "## Gross Description:\n") \
#                                             .replace("Microscopic Examination:", "## Microscopic Examination:\n") \
#                                             .replace("Diagnosis:", "## Diagnosis:\n") \
#                                             .replace("Comments:", "## Comments:\n") \
#                                             .replace("Radiological Findings:", "## Radiological Findings:\n") \
#                                             .replace("Procedure:", "## Procedure:\n") \
#                                             .replace("Recommendations:", "## Recommendations:\n") \
#                                             .replace("Preliminary Pathology Remarks:", "## Preliminary Pathology Remarks:\n")

#         # Display the organized pathology report
#         st.subheader("Organized Pathology Report")
#         st.markdown(organized_report)

import streamlit as st
from dotenv import load_dotenv
import os
from PIL import Image
import pytesseract
import openai
import fitz  # PyMuPDF

load_dotenv()  # Load environment variables from .env file
openai.api_key = os.getenv('OPENAI_API_KEY')


# Streamlit App Layout
st.title("Medical Report Reformatter")
st.write("Upload an image or PDF of a medical report, and we will reformat it professionally as a pathology report.")

# Initialize extracted text variables
extracted_text_image = ""
extracted_text_pdf = ""
pytesseract.pytesseract.tesseract_cmd = "pytesseract"
# Upload image
uploaded_image = st.file_uploader("Upload an image...", type=["jpg", "jpeg", "png"])

if uploaded_image is not None:
    # Display the uploaded image
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Extract text using Tesseract OCR
    with st.spinner("Extracting text from the image..."):
        extracted_text_image = pytesseract.image_to_string(image)

    st.subheader("Extracted Text from Image")
    st.write(extracted_text_image)

# Upload PDF
uploaded_pdf = st.file_uploader("Upload a PDF...", type=["pdf"])

if uploaded_pdf is not None:
    # Read PDF file from the uploaded file stream
    with st.spinner("Extracting text from the PDF..."):
        pdf_document = fitz.open(stream=uploaded_pdf.read(), filetype="pdf")
        extracted_text_pdf = ""
        
        # Extract text from all pages
        for page in pdf_document:
            extracted_text_pdf += page.get_text() + "\n"  # Append text from each page
        
        pdf_document.close()

    st.subheader("Extracted Text from PDF")
    st.write(extracted_text_pdf)

# Combine extracted text
extracted_text = extracted_text_image + extracted_text_pdf

# Text area for user to edit the extracted text
if extracted_text:
    st.subheader("Edit Extracted Text")
    edited_text = st.text_area("You can edit the extracted text below before generating the report:", value=extracted_text, height=300)

    # Define a prompt for GPT to rewrite the text as a pathology report
    prompt = f"""
    You are a professional pathology doctor. Below is a raw medical report extracted from an image or PDF.
    Please reformat it into a structured pathology report with proper sections: Patient Details, 
    Clinical History, Gross Description, Microscopic Examination, Diagnosis, Comments, 
    Radiological Findings, Procedure, Recommendations, and Preliminary Pathology Remarks.

    Raw Medical Report:
    {edited_text}
    
    Rewritten Pathology Report:
    """

    if st.button("Generate Pathology Report"):
        with st.spinner("Generating professional pathology report..."):
            # OpenAI GPT API call to reformat the extracted text
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            formatted_report = response.choices[0].message['content']

        # Organize the generated report into sections
        organized_report = formatted_report.replace("Patient Details:", "## Patient Details:\n") \
                                            .replace("Clinical History:", "## Clinical History:\n") \
                                            .replace("Gross Description:", "## Gross Description:\n") \
                                            .replace("Microscopic Examination:", "## Microscopic Examination:\n") \
                                            .replace("Diagnosis:", "## Diagnosis:\n") \
                                            .replace("Comments:", "## Comments:\n") \
                                            .replace("Radiological Findings:", "## Radiological Findings:\n") \
                                            .replace("Procedure:", "## Procedure:\n") \
                                            .replace("Recommendations:", "## Recommendations:\n") \
                                            .replace("Preliminary Pathology Remarks:", "## Preliminary Pathology Remarks:\n")

        # Display the organized pathology report
        st.subheader("Organized Pathology Report")
        st.markdown(organized_report)
