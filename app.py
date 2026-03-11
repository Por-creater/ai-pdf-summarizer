import streamlit as st
import pdfplumber
import google.generativeai as genai

# ===== API KEY =====
genai.configure(api_key="AIzaSyCWJ4EfPOYhFdHRrrEx7RHeSq51y8lUzHc")

# ===== UI =====
st.title("📄 AI PDF Summarizer")
st.write("Upload a PDF and let AI summarize it.")

uploaded_file = st.file_uploader("Upload PDF", type="pdf")

if uploaded_file:

    st.success("PDF uploaded successfully!")

    text = ""

    # อ่าน PDF
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text

    if len(text) == 0:
        st.error("Cannot extract text from this PDF")

    else:
        text = text[:15000]

        if st.button("Generate Summary"):

            with st.spinner("AI is summarizing..."):

                try:

                    model = genai.GenerativeModel("gemini-2.5-flash")

                    response = model.generate_content(
                        f"Summarize this document in bullet points:\n{text}"
                    )

                    st.subheader("📌 Summary")
                    st.write(response.text)

                except Exception as e:
                    st.error("Error occurred")
                    st.write(e)
