import streamlit as st
import pdfplumber
import google.generativeai as genai

genai.configure(api_key="AIzaSyCWJ4EfPOYhFdHRrrEx7RHeSq51y8lUzHc")

st.title("AI PDF Summarizer")

uploaded_file = st.file_uploader("Upload PDF", type="pdf")

if uploaded_file:

    text = ""   # ต้องมีบรรทัดนี้ก่อน

    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text

    text = text[:12000]

    if st.button("Summarize"):

        model = genai.GenerativeModel("gemini-1.5-flash")

        response = model.generate_content(
            f"Summarize this document:\n{text}"
        )

        st.subheader("Summary")
        st.write(response.text)
