import os
import re
import pytesseract
from pdf2image import convert_from_path
from PIL import ImageEnhance

def extract_text_from_pdf(pdf_path):
    # Convert PDF to high-quality grayscale images
    images = convert_from_path(pdf_path, dpi=400, grayscale=True)
    full_text = []
    for image in images:
        # Enhance image clarity
        enhancer = ImageEnhance.Sharpness(image)
        image = enhancer.enhance(2.0)
        text = pytesseract.image_to_string(image)
        full_text.append(text)
    return "\n".join(full_text).upper()

def parse_documents(pdf_directory):
    signed_names = []
    dear_pattern = re.compile(r'DEAR\s+([A-Z][A-Z\s]+?)(?:\n|,)', re.DOTALL)
    signature_pattern = re.compile(r'SIGNATURE:\s*\S+', re.IGNORECASE)

    for filename in os.listdir(pdf_directory):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(pdf_directory, filename)
            text = extract_text_from_pdf(pdf_path)

            dear_match = dear_pattern.search(text)
            if not dear_match:
                continue
            name = dear_match.group(1).replace('\n', ' ').strip()

            if signature_pattern.search(text):
                signed_names.append(name)
    
    return [f"{i+1}. {name}" for i, name in enumerate(signed_names)]

# Example usage
pdf_directory = "./pdfs"
signed_list = parse_documents(pdf_directory)
print("Here are the Signed Documents:")
print("\n".join(signed_list) if signed_list else "No signed documents found")
