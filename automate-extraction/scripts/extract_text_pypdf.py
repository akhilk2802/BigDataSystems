from PyPDF2 import PdfReader
import os
import json
from utils.logging_module import log_info, log_error

def extract_text_pypdf():
    output_dir = "../extracted_texts/pypdf"
    os.makedirs(output_dir, exist_ok=True)
    
    extracted_texts = []

    pdf_dir = "../downloaded_pdfs"

    for file in os.listdir(pdf_dir):
        if file.endswith('.pdf'):
            base_file_name = os.path.splitext(file)[0]
            output_file = os.path.join(output_dir, f"{base_file_name}.json")

            try:
                file_path = os.path.join(pdf_dir, file)
                reader = PdfReader(file_path)
                pypdf_text = "".join([page.extract_text() for page in reader.pages])

                # Save extracted text
                with open(output_file, 'w') as f:
                    json.dump({"file_name": file, "text": pypdf_text}, f)
                log_info(f"Extracted text from {file} using PyPDF2 to {output_file}")
                extracted_texts.append(output_file)
            except Exception as e:
                log_error(f"Failed to extract text from {file} using PyPDF2: {e}")

    return extracted_texts