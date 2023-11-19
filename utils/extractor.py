import PyPDF2
import docx
import csv
import openpyxl


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as pdf_file:
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)
        for page_num in range(pdf_reader.numPages):
            page = pdf_reader.getPage(page_num)
            text += page.extractText()
    return text


def extract_text_from_docx(docx_path):
    doc = docx.Document(docx_path)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text
    return text


def extract_text_from_csv(csv_path):
    with open(csv_path, "r", encoding="utf-8") as csv_file:
        csv_reader = csv.reader(csv_file)
        text = "\n".join(",".join(row) for row in csv_reader)
    return text


def extract_text_from_txt(txt_path):
    with open(txt_path, "r", encoding="utf-8") as txt_file:
        text = txt_file.read()
    return text


def extract_file(filename, file_path):
    if file.filename.endswith(".pdf"):
        text = extract_text_from_pdf(file_path)
    elif file.filename.endswith(".docx"):
        text = extract_text_from_docx(file_path)
    elif file.filename.endswith(".csv"):
        text = extract_text_from_csv(file_path)
    elif file.filename.endswith((".txt", ".log")):
        text = extract_text_from_txt(file_path)
    else:
        text = "Unsupported file format"

    return text
