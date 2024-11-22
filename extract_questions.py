import os 
from PyPDF2 import PdfReader
from docx import Document
import csv

files_folder = "files/"
all_questions = []

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text

def extract_text_from_docx(docx_path):
    text = ""
    doc = Document(docx_path)
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text

for (folders, labels, files) in os.walk(files_folder):
    for file in files:
        full_file_path = f"{files_folder}{file}"
        print(full_file_path)

        if full_file_path.endswith('.pdf'):
            all_questions.append({
                "file_name": file,
                "content": extract_text_from_pdf(full_file_path)
            })
        elif full_file_path.endswith('.docx'):
            all_questions.append({
                "file_name": file,
                "content": extract_text_from_docx(full_file_path)
            })

with open("questions.csv", "w") as csv_output_file:
    csv_writer = csv.writer(csv_output_file)
    csv_writer.writerow(["name", "text_content"])

    for question in all_questions:
        csv_writer.writerow([question["file_name"], question["content"]])