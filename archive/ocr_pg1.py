"""
This module extracts dates from PDF files by performing OCR on the first page.
It uses PyMuPDF to open the PDF and pytesseract to perform OCR on images.
The extracted dates are saved to a CSV file, and the OCR text for files without dates is saved to a debug file.
"""
import os
import fitz  # PyMuPDF: Library for working with PDFs
import pytesseract  # Tesseract OCR for extracting text from images
from PIL import Image  # Pillow for handling images
import io
import re

def ocr_image(image_bytes):
    """
    Perform OCR (Optical Character Recognition) on an image.

    Args:
        image_bytes (bytes): Image data in bytes format.

    Returns:
        str: Extracted text from the image using Tesseract OCR.
    """
    image = Image.open(io.BytesIO(image_bytes))  # Convert bytes to a PIL image
    text = pytesseract.image_to_string(image)   # Perform OCR on the image
    return text

def extract_and_ocr_images_from_first_page(pdf_path):
    """
    Extract and perform OCR on all images found on the first page of a PDF.

    Args:
        pdf_path (str): Path to the PDF file.

    Returns:
        str: Combined OCR text extracted from all images on the first page.
    """
    doc = fitz.open(pdf_path)  # Open the PDF file
    first_page = doc[0]  # Access the first page
    image_list = first_page.get_images(full=True)  # Get all images on the page
    
    ocr_results = []
    for img in image_list:
        xref = img[0]  # Reference to the image
        base_image = doc.extract_image(xref)  # Extract image details
        image_bytes = base_image["image"]  # Get the image data in bytes
        ocr_text = ocr_image(image_bytes)  # Perform OCR on the image
        ocr_results.append(ocr_text)
    
    doc.close()  # Close the PDF file
    return "\n".join(ocr_results)  # Combine all extracted OCR text

def identify_and_normalize_date(date_str):
    """
    Identify and normalize a date string to 'DD-MM-YYYY' format.

    Args:
        date_str (str): Input date string.

    Returns:
        str: Normalized date in 'DD-MM-YYYY' format if found, otherwise 'Date not found'.
    """
    # Define patterns to search for dates in various formats
    patterns = [
        r'(\d{2})[-\/\.]?(\d{2})[-\/\.]?(\d{4})',  # DD-MM-YYYY or DD/MM/YYYY
        r'(\d{4})[-\/\.]?(\d{2})[-\/\.]?(\d{2})'   # YYYY-MM-DD or YYYY/MM/DD
    ]
    
    for pattern in patterns:
        match = re.search(pattern, date_str)
        if match:
            # If year is the first group, rearrange to DD-MM-YYYY
            if len(match.group(1)) == 4:  
                year, month, day = match.group(1), match.group(2), match.group(3)
            else:  # Assume DD-MM-YYYY format
                day, month, year = match.group(1), match.group(2), match.group(3)
            
            # Return date in standardized format
            return f"{day.zfill(2)}-{month.zfill(2)}-{year.zfill(4)}"
    
    return "Date not found"

def extract_date_from_text(text):
    """
    Extract the first date occurrence from the OCR text.
    - Priority is given to the "Date Printed" pattern.
    - If not found, a generic date search is performed.

    Args:
        text (str): OCR text from the PDF.

    Returns:
        str: Normalized date if found, otherwise 'Date not found'.
    """
    # Look for "Date Printed" pattern followed by a date
    date_pattern = re.compile(r'Date Printed:?\s*([\d\-\/.\s]{10,})')
    match = date_pattern.search(text)
    
    if match:
        date_str = match.group(1).strip()[:10]  # Extract 10 characters after "Date Printed"
        normalized_date = identify_and_normalize_date(date_str)
        if normalized_date != "Date not found":
            return normalized_date
    
    # If "Date Printed" is not found, search for any generic DD-MM-YYYY date
    generic_date_pattern = re.compile(r'(\d{2})[-\/\.](\d{2})[-\/\.](\d{4})')
    match = generic_date_pattern.search(text)
    if match:
        return f"{match.group(1)}-{match.group(2)}-{match.group(3)}"
    
    return "Date not found"

def process_pdfs_and_generate_csv(folder_path, csv_file, debug_text_file):
    """
    Process all PDFs in a folder to extract dates from images on the first page.
    - Writes results to a CSV file.
    - Saves OCR text for PDFs without identifiable dates to a debug file.

    Args:
        folder_path (str): Path to the folder containing PDF files.
        csv_file (str): Path to the output CSV file.
        debug_text_file (str): Path to the debug text file for manual review.
    """
    with open(csv_file, "w", encoding="utf-8") as csv_output:
        csv_output.write("Filename,Date Printed\n")  # Write CSV header
        
        with open(debug_text_file, "w", encoding="utf-8") as debug_output:
            for filename in os.listdir(folder_path):
                if filename.lower().endswith(".pdf"):  # Process only PDF files
                    pdf_path = os.path.join(folder_path, filename)
                    
                    # Print the file name to the console for progress tracking
                    print(f"Processing: {filename}")
                    
                    # Perform OCR on the first page images
                    ocr_text = extract_and_ocr_images_from_first_page(pdf_path)
                    
                    if ocr_text.strip():
                        # Extract date from the OCR text
                        date_extracted = extract_date_from_text(ocr_text)
                        csv_output.write(f"{filename},{date_extracted}\n")  # Write to CSV
                        
                        # Save full OCR text for files without identifiable dates
                        if date_extracted == "Date not found":
                            debug_output.write(f"Filename: {filename}\n")
                            debug_output.write(f"OCR Text:\n{ocr_text}\n\n")
                    else:
                        # Handle case where no text is extracted
                        csv_output.write(f"{filename},No text extracted\n")
                        debug_output.write(f"Filename: {filename}\n")
                        debug_output.write("OCR Text: No text extracted\n\n")

# Example usage
if __name__ == "__main__":
    # This is the main section of the script.
    # It defines the folder path, CSV file, and debug text file paths.
    # Before running this script, make sure to install the required libraries:
    # pip install PyMuPDF pytesseract Pillow
    folder_path = "pdf"  # Path to the folder containing PDFs
    csv_file = "wo_starts.csv"  # Output CSV file to save extracted dates
    debug_text_file = "wo_debug_text.txt"  # Debug text file for manual inspection
    
    process_pdfs_and_generate_csv(folder_path, csv_file, debug_text_file)
    print(f"Date extraction results have been written to {csv_file}")
    print(f"Any WO debug text for files without dates has been written to {debug_text_file}")
