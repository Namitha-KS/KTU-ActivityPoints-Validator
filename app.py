# import streamlit as st
# import nltk
# from nltk.tokenize import word_tokenize
# from nltk.corpus import stopwords
# from PIL import Image
# import easyocr
# import numpy as np
# import PyPDF2

# # Download NLTK stopwords resource (if not already downloaded)
# nltk.download('stopwords')

# # Define stopwords for NLTK
# stop_words = set(stopwords.words("english"))

# # Initialize the OCR reader
# reader = easyocr.Reader(['en'])

# # Streamlit app
# def main():
#     st.title("KTU Activity Points Validator")

#     uploaded_file = st.file_uploader("Choose a PDF file or a screenshot image", type=["pdf", "png", "jpg", "jpeg"])

#     if uploaded_file is not None:
#         if uploaded_file.type == 'application/pdf':
#             # Load PDF and extract text
#             text = ""
#             pdf_reader = PyPDF2.PdfFileReader(uploaded_file)
#             for page in range(pdf_reader.getNumPages()):
#                 text += pdf_reader.getPage(page).extractText()

#         elif uploaded_file.type in ['image/png', 'image/jpeg', 'image/jpg']:
#             # Read text from the image using easyocr
#             image = Image.open(uploaded_file)
#             result = reader.readtext(np.array(image))
#             text = ' '.join([entry[1] for entry in result])
#         else:
#             st.write("Unsupported file type. Please upload a PDF or an image (png, jpg, jpeg).")
#             return

#         # Tokenize and filter text
#         words = word_tokenize(text)
#         filtered_text = [word for word in words if word.casefold() not in stop_words]

#         # Check if the word "internship" is in the content
#         if "internship" in filtered_text:
#             st.write("Activity Points: 10")  # Assuming 10 points for internship
#         else:
#             st.write("No activity points found for 'internship'")

# if __name__ == "__main__":
#     main()


from flask import Flask, render_template, request
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from PIL import Image
import easyocr
import numpy as np
import PyPDF2

# Download NLTK stopwords resource (if not already downloaded)
nltk.download('stopwords')

# Define stopwords for NLTK
stop_words = set(stopwords.words("english"))

# Initialize the OCR reader
reader = easyocr.Reader(['en'])

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_upload', methods=['POST'])
def process_upload():
    uploaded_file = request.files['fileUpload']

    if uploaded_file.filename != '':
        if uploaded_file.filename.endswith('.pdf'):
            # Load PDF and extract text
            text = ""
            pdf_reader = PyPDF2.PdfFileReader(uploaded_file)
            for page in range(pdf_reader.getNumPages()):
                text += pdf_reader.getPage(page).extractText()
        elif uploaded_file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            # Read text from the image using easyocr
            image = Image.open(uploaded_file)
            result = reader.readtext(np.array(image))
            text = ' '.join([entry[1] for entry in result])
        else:
            return "Unsupported file type. Please upload a PDF or an image (png, jpg, jpeg)."

        # Tokenize and filter text
        words = word_tokenize(text)
        filtered_text = [word for word in words if word.casefold() not in stop_words]

        # Check if the word "internship" is in the content
        if "internship" in filtered_text:
            return "Activity Points: 20"  # Assuming 10 points for internship
        else:
            return "No activity points found for 'internship'"
    else:
        return "No file uploaded"

if __name__ == '__main__':
    app.run(debug=True)
