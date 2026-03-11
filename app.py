import streamlit as st
import pdfplumber
import google.generativeai as genai

# ====== ตั้งค่า API KEY ======
# สำหรับทดสอบสามารถใส่ตรงนี้ได้ก่อน
genai.configure(api_key="YOUR_API_KEY")

# ====== UI ======
st.title("📄 AI PDF Summarizer")
st.write("Upload a PDF and let AI summarize it.")

uploaded_file = st.file_uploader("Upload PDF", type="pdf")

if uploaded_file is not None:

    st.success("PDF uploaded successfully!")

    # ====== อ่าน PDF ======
    text = ""

    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text

    # จำกัดขนาดข้อความ
    text = text[:12000]

    st.info("PDF text extracted")

    if st.button("Generate Summary"):

        with st.spinner("AI is summarizing..."):

            try:
                model = genai.GenerativeModel("gemini-1.5-flash")

                response = model.generate_content(
                    f"Summarize this document in bullet points:\n{text}"
                )

                st.subheader("📌 Summary")

                st.write(response.text)

            except Exception as e:
                st.error("Error occurred")
                st.write(e)
