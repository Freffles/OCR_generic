"""
This module extracts text and dates from PDF files.
It uses PyMuPDF for PDF processing and pytesseract for OCR when needed.
The extracted data is saved to a CSV file.
"""
import os
import fitz  # PyMuPDF: Library for working with PDFs
import pytesseract  # Tesseract OCR for image text extraction
from PIL import Image  # Pillow for image handling
import csv
import re
from datetime import datetime


def extract_text_from_first_page(pdf_path):
    """
    Extract text from the first page of a PDF.
    - If no text is found (likely a scanned image), fallback to OCR.

    Args:
        pdf_path (str): Path to the PDF file.

    Returns:
        str: Extracted text from the first page.
    """
    # Open the PDF file
    doc = fitz.open(pdf_path)
    # Get the first page
    page = doc[0]
    # Attempt to extract text directly
    text = page.get_text()

    # Fallback to OCR if no text is extracted
    if not text.strip():
        # Convert the first page to an image (RGB format)
        pix = page.get_pixmap()
        image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        # Use Tesseract OCR to extract text from the image
        text = pytesseract.image_to_string(image)
    doc.close()
    return text


def save_text_to_file(pdf_path, text, debug_file):
    """
    Save the extracted text to a debug output file for inspection.

    Args:
        pdf_path (str): Path to the PDF file being processed.
        text (str): Extracted text to save.
        debug_file (str): Path to the debug text file.
    """
    # Open the debug file in append mode
    with open(debug_file, 'a', encoding='utf-8') as file:
        # Write the file name for context
        file.write(f"File: {os.path.basename(pdf_path)}\n")
        # Write the extracted text or a placeholder if no text was found
        if text:
            file.write(text + "\n")
        else:
            file.write("[No text extracted]\n")
        # Add a separator for readability
        file.write("=" * 40 + "\n")


def normalize_date(date_str):
    """
    Normalize a date string into 'DD-MM-YYYY' format.
    - Replaces all non-numeric characters with hyphens.
    - Handles both 'DD-MM-YYYY' and 'DD-MM-YY' formats.

    Args:
        date_str (str): Candidate date string to normalize.

    Returns:
        str or None: Normalized date in 'DD-MM-YYYY' format, or None if invalid.
    """
    # Replace any non-numeric characters with hyphens
    date_str = re.sub(r'[^0-9]', '-', date_str)
    try:
        # Attempt to parse as 'DD-MM-YYYY'
        date_obj = datetime.strptime(date_str, "%d-%m-%Y")
        return date_obj.strftime("%d-%m-%Y")
    except ValueError:
        try:
            # Attempt to parse as 'DD-MM-YY'
            date_obj = datetime.strptime(date_str, "%d-%m-%y")
            return date_obj.strftime("%d-%m-%Y")
        except ValueError:
            return None


def extract_date_from_text(text):
    """
    Extract the first occurrence of a date string from the text.
    - Searches for lines containing "Date Printed".
    - Extracts and normalizes the date immediately following this phrase.

    Args:
        text (str): Extracted text from the PDF.

    Returns:
        str or None: Normalized date if found, otherwise None.
    """
    # Process each line of the text to search for 'Date Printed'
    for line in text.splitlines():
        if "Date Printed" in line:
            # Find where "Date Printed" ends
            start_index = line.index("Date Printed") + len("Date Printed")
            # Skip over a colon if it appears directly after the phrase
            if line[start_index] == ':':
                start_index += 1  # Move past the colon
            # Skip over any spaces after "Date Printed"
            start_index += 1  

            # Extract the next 10 characters as the potential date
            date_candidate = line[start_index:start_index + 10].strip()

            # Normalize the date and return it
            normalized_date = normalize_date(date_candidate)
            return normalized_date
    return None


def process_pdfs_and_generate_csv(folder_path, csv_file, debug_file):
    """
    Process all PDF files in a folder:
    - Extract text from the first page (or fallback to OCR).
    - Extract a 'Date Printed' value if present.
    - Save results to a CSV file and write full extracted text to a debug file.

    Args:
        folder_path (str): Path to the folder containing PDF files.
        csv_file (str): Path to the output CSV file.
        debug_file (str): Path to the debug text file.
    """
    # Open the CSV file for writing
    with open(csv_file, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        # Write the header row
        csvwriter.writerow(['filename', 'date'])

        # Iterate through all files in the folder
        for filename in os.listdir(folder_path):
            # Process only PDF files
            if filename.lower().endswith('.pdf'):
                pdf_path = os.path.join(folder_path, filename)

                # Extract text from the first page
                text = extract_text_from_first_page(pdf_path)
                # Save the full text to the debug file
                save_text_to_file(pdf_path, text, debug_file)
                # Extract the date from the text
                date = extract_date_from_text(text)
                # Write the filename and extracted date to the CSV file
                csvwriter.writerow([filename, date])


# Example usage
if __name__ == "__main__":
    # This is the main section of the script.
    # It defines the folder path, CSV file, and debug file paths.
    # Before running this script, make sure to install the required libraries:
    # pip install PyMuPDF pytesseract Pillow
    folder_path = "pdf"  # Path to folder containing PDFs (update as needed)
    csv_file = "PyMuPDF_output.csv"  # Output CSV file path
    debug_file = "PyMuPDF_debug_output.txt"  # Debug text file path

    process_pdfs_and_generate_csv(folder_path, csv_file, debug_file)
    print(f"Date extraction results have been saved to {csv_file}")
    print(f"Full text outputs have been saved to {debug_file}")
