import fitz
import pandas as pd

def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    text = "\n".join(page.get_text() for page in doc)
    return text

def extract_text_from_excel(file_path):
    df = pd.read_excel(file_path)
    return "\n".join(df.astype(str).apply(lambda x: ' '.join(x), axis=1))

def extract_text_from_csv(file_path):
    df = pd.read_csv(file_path)
    return "\n".join(df.astype(str).apply(lambda x: ' '.join(x), axis=1))
