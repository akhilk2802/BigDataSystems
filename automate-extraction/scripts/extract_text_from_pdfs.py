from PyPDF2 import PdfReader
# from unstructured.partition.pdf import partition_pdf
from unstructured.partition.auto import partition

import os
import json
from utils.logging_module import log_info, log_error

def extract_text_from_pdfs():
    extracted_texts = []
    

    output_dir_pypdf = "../../automate-extraction/extracted_texts/pypdf"
    os.makedirs(output_dir_pypdf, exist_ok=True)

    output_dir_unstructured = "../../automate-extraction/extracted_texts/pypdf"
    os.makedirs(output_dir_unstructured, exist_ok=True)

    # Directory where the PDFs are downloaded
    pdf_dir = "../../downloaded_pdfs"
    
    for file in os.listdir(pdf_dir):
        if file.endswith('.pdf'):
            base_file_name = os.path.splitext(file)[0]
            pypdf_output_file = os.path.join(output_dir_pypdf, f"{base_file_name}.json")
            unstructured_output_file = os.path.join(output_dir_unstructured, f"{base_file_name}.json")

            try:
                # PyPDF2 Extraction
                file_path = os.path.join(pdf_dir, file)
                reader = PdfReader(file_path)
                # reader = PdfReader(file)
                pypdf_text = "".join([page.extract_text() for page in reader.pages])
                
                # Save PyPDF2 extracted text
                with open(pypdf_output_file, 'w') as f:
                    json.dump({"file_name": file, "text": pypdf_text}, f)
                log_info(f"Extracted text from {file} using PyPDF2 to {pypdf_output_file}")
                extracted_texts.append(pypdf_output_file)

            except Exception as e:
                log_error(f"Failed to extract text from {file} using PyPDF2: {e}")
            
            # try:
            #     # Unstructured Library Extraction
            #     unstructured_text = partition_pdf(filename=file_path)
            #     unstructured_content = " ".join([elem.text for elem in unstructured_text if elem.text])
                
            #     # Save Unstructured extracted text
            #     with open(unstructured_output_file, 'w') as f:
            #         json.dump({"file_name": file, "text": unstructured_content}, f)
            #     log_info(f"Extracted text from {file} using Unstructured to {unstructured_output_file}")
            #     extracted_texts.append(unstructured_output_file)
            # except Exception as e:
            #     log_error(f"Failed to extract text from {file} using Unstructured: {e}")

            try:
                # Unstructured Library Extraction
                # unstructured_text = partition_pdf(filename=file_path)
                unstructured_text = partition(filename=file_path)
                unstructured_content = " ".join([elem.text for elem in unstructured_text if elem.text])
                with open(unstructured_output_file, 'w') as f:
                    json.dump({"file_name": file, "text": unstructured_content}, f)
                log_info(f"Extracted text from {file} using Unstructured to {unstructured_output_file}")
            except Exception as e:
                log_error(f"Failed to extract text from {file} using Unstructured: {e}")
    return extracted_texts