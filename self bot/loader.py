import os
from pypdf import PdfReader
import docx

def load_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def load_pdf(file_path):
    reader = PdfReader(file_path)
    return "\n".join([page.extract_text() or "" for page in reader.pages])

def load_docx(file_path):
    doc = docx.Document(file_path)
    return "\n".join([p.text for p in doc.paragraphs])

def load_single_file(file_path):
    if file_path.endswith(".txt"):
        return load_txt(file_path)
    elif file_path.endswith(".pdf"):
        return load_pdf(file_path)
    elif file_path.endswith(".docx"):
        return load_docx(file_path)
    return ""

def load_knowledge_base(folder_path):
    texts = []
    for filename in os.listdir(folder_path):
        full_path = os.path.join(folder_path, filename)
        texts.append(load_single_file(full_path))
    return texts
