import os
import fitz
from docx import Document
import text_extract as te

def extract_text_from_pdf(file_path):
    ext = os.path.splitext(file_path)[1].lower()

    if ext == '.pdf':
        with fitz.open(file_path) as pdf:
            return "\n".join(page.get_text() for page in pdf)
        
    elif ext == '.docx':
        doc = Document(file_path)
        return "\n".join([paragraph.text for paragraph in doc.paragraphs if paragraph.text.strip()])
    
    elif ext == '.doc':
        text = te.extract_text_from_pdf(file_path)
        return text.strip()
    
    else:
        raise ValueError("Unsupported file format: {}".format(ext))