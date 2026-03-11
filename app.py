from flask import Flask, render_template, request
import pdfplumber
import google.generativeai as genai

genai.configure(api_key="AIzaSyCWJ4EfPOYhFdHRrrEx7RHeSq51y8lUzHc")

model = genai.GenerativeModel("gemini-pro")

app = Flask(__name__)

def extract_text(pdf):
    text = ""
    with pdfplumber.open(pdf) as pdf_file:
        for page in pdf_file.pages:
            text += page.extract_text()
    return text

def summarize(text):
    prompt = f"Summarize this document in bullet points:\n{text}"
    response = model.generate_content(prompt)
    return response.text

@app.route("/", methods=["GET","POST"])
def index():

    summary = ""

    if request.method == "POST":

        file = request.files["pdf"]

        text = extract_text(file)

        summary = summarize(text)

    return render_template("index.html", summary=summary)

if __name__ == "__main__":
    app.run(debug=True)