"""
This script extracts text from the first page of a PDF file using OCR (Optical Character Recognition).
It uses the PyMuPDF library to open and render the PDF page as an image,
and the pytesseract library to perform OCR on that image.
"""
# 0wo_extract.py
# This script extracts text from the first page of a PDF file using OCR (Optical Character Recognition).
# It uses the PyMuPDF library to open and render the PDF page as an image,
# and the pytesseract library to perform OCR on that image.

import fitz  # PyMuPDF library for PDF processing
import pytesseract  # pytesseract library for OCR
from PIL import Image  # Python Imaging Library for image handling

def extract_text_from_first_page(pdf_path):
    """
    Extracts text from the first page of a given PDF file using OCR.

    Args:
        pdf_path (str): The path to the PDF file.

    Returns:
        str: The extracted text from the first page of the PDF.
    """
    # Open the PDF file using PyMuPDF.
    doc = fitz.open("101207_1_130 as at 09-01-20.pdf")

    # Get the first page of the PDF document (index 0).
    page = doc[0]

    # Render the page to a pixmap (image).
    pix = page.get_pixmap()
    
    # Create a PIL Image object from the pixmap data.
    image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

    # Perform OCR on the image using pytesseract to extract the text.
    text = pytesseract.image_to_string(image)

    # Close the PDF document.
    doc.close()

    # Return the extracted text.
    return text

# Example of how to use the function:
pdf_path = "example.pdf"
print(extract_text_from_first_page(pdf_path))
