"""
This module extracts text and dates from PDF files using PyPDF2 and PyMuPDF.
It falls back to OCR if direct text extraction fails.
The extracted data is saved to a CSV file.
"""
import os
import PyPDF2  # Library for extracting text from PDF files
import fitz  # PyMuPDF: Library for working with PDFs as images
import pytesseract  # Tesseract OCR for text extraction from images
from PIL import Image, ImageFilter  # Pillow library for image handling
import csv  # For writing extracted data to CSV
import re  # Regular expressions for date extraction
from datetime import datetime  # For normalizing date formats


def extract_text_from_first_page(pdf_path):
    """
    Extract text from the first page of a PDF using PyPDF2.
    Falls back to OCR if PyPDF2 fails to extract text.

    Args:
        pdf_path (str): Path to the PDF file.

    Returns:
        str: Extracted text from the first page.
    """
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        page = reader.pages[0]  # Access the first page

        # Attempt to extract text using PyPDF2
        text = page.extract_text()
        if text:
            print(f"Extracted Text for {pdf_path}:\n{text[:200]}...\n")  # Preview extracted text
            return text
        else:
            print(f"No text extracted for {pdf_path} with PyPDF2. Trying OCR.")
            # Fall back to OCR
            text = extract_text_with_ocr(pdf_path)
            return text


def enhance_image_for_ocr(image):
    """
    Enhance an image for better OCR results by converting to grayscale and reducing noise.

    Args:
        image (PIL.Image): Original image to enhance.

    Returns:
        PIL.Image: Enhanced grayscale image.
    """
    # Rotate the image (if required)
    rotated_image = image.rotate(270, expand=True)
    # Convert to grayscale
    gray_image = rotated_image.convert('L')
    # Apply Gaussian blur to reduce noise
    blurred_image = gray_image.filter(ImageFilter.GaussianBlur(1))
    return blurred_image


def extract_text_with_ocr(pdf_path):
    """
    Perform OCR on the first page of a PDF to extract text.

    Args:
        pdf_path (str): Path to the PDF file.

    Returns:
        str: Text extracted using OCR.
    """
    # Open the PDF with PyMuPDF
    doc = fitz.open(pdf_path)
    page = doc.load_page(0)  # Load the first page
    # Convert the page to an image
    pix = page.get_pixmap()
    image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

    # Enhance the image for better OCR results
    enhanced_image = enhance_image_for_ocr(image)
    # Extract text using Tesseract OCR
    text = pytesseract.image_to_string(enhanced_image)
    doc.close()

    # Print preview of the OCR results
    if text.strip():
        print(f"OCR Extracted Text for {pdf_path}:\n{text[:200]}...\n")
    else:
        print(f"OCR also failed for {pdf_path}.")
    return text


def save_text_to_file(pdf_path, text, debug_file):
    """
    Save extracted text from a PDF to a debug output file.

    Args:
        pdf_path (str): Path to the PDF file.
        text (str): Extracted text content.
        debug_file (str): Path to the debug output file.
    """
    with open(debug_file, 'a', encoding='utf-8') as file:
        file.write(f"File: {os.path.basename(pdf_path)}\n")
        if text:
            file.write(text + "\n")
        else:
            file.write("[No text extracted]\n")
        file.write("=" * 40 + "\n")  # Add separator for readability


def normalize_date(date_str):
    """
    Normalize a date string to 'DD-MM-YYYY' format.

    Args:
        date_str (str): Candidate date string to normalize.

    Returns:
        str or None: Normalized date in 'DD-MM-YYYY' format if valid, else None.
    """
    # Replace all non-numeric characters with hyphens
    date_str = re.sub(r'[^0-9]', '-', date_str)
    try:
        date_obj = datetime.strptime(date_str, "%d-%m-%Y")
        return date_obj.strftime("%d-%m-%Y")
    except ValueError:
        try:
            date_obj = datetime.strptime(date_str, "%d-%m-%y")
            return date_obj.strftime("%d-%m-%Y")
        except ValueError:
            return None


def extract_date_from_text(text):
    """
    Extract the first 'Date Printed' occurrence from the text.

    Args:
        text (str): Text content to search for the date.

    Returns:
        str or None: Normalized date if found, otherwise None.
    """
    for line in text.splitlines():
        if "Date Printed" in line:
            start_index = line.index("Date Printed") + len("Date Printed")
            # Handle optional colon
            if line[start_index] == ':':
                start_index += 1
            start_index += 1  # Skip space

            # Extract 10 characters following 'Date Printed'
            date_candidate = line[start_index:start_index + 10].strip()
            normalized_date = normalize_date(date_candidate)
            return normalized_date
    return None


def process_pdfs_and_generate_csv(folder_path, csv_file, debug_file):
    """
    Process all PDFs in a folder, extract text, find dates, and write results to a CSV file.

    Args:
        folder_path (str): Path to the folder containing PDF files.
        csv_file (str): Path to the output CSV file.
        debug_file (str): Path to the debug text file.
    """
    with open(csv_file, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['filename', 'date'])  # Write header row

        for filename in os.listdir(folder_path):
            if filename.lower().endswith('.pdf'):  # Process only PDF files
                pdf_path = os.path.join(folder_path, filename)
                print(f"Processing file: {filename}")
                # Extract text from the PDF
                text = extract_text_from_first_page(pdf_path)
                # Save full extracted text to debug file
                save_text_to_file(pdf_path, text, debug_file)
                # Extract date from the text
                date = extract_date_from_text(text)
                # Write results to CSV
                csvwriter.writerow([filename, date])


# Example usage
if __name__ == "__main__":
    # This is the main section of the script.
    # It defines the folder path, CSV file, and debug file paths.
    # Before running this script, make sure to install the required libraries:
    # pip install PyPDF2 PyMuPDF pytesseract Pillow
    folder_path = "pdf"  # Path to folder containing PDF files
    csv_file = "output.csv"  # Output CSV file
    debug_file = "output.txt"  # Debug text file

    process_pdfs_and_generate_csv(folder_path, csv_file, debug_file)
    print(f"Date extraction results saved to {csv_file}")
    print(f"Full OCR text outputs saved to {debug_file}")
