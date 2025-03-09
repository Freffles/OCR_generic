"""
This module provides functions for extracting text from PDF files using OCR.
It includes functions for enhancing images, performing OCR, and saving the extracted text.
"""
import fitz  # PyMuPDF: Library for working with PDFs
import pytesseract  # Tesseract OCR for text extraction from images
from PIL import Image  # Pillow library for image processing
import io  # For handling byte streams
import os  # For file and folder operations

def enhance_image_for_ocr(image_bytes):
    """
    Enhance an image for better OCR results by converting it to grayscale.

    Args:
        image_bytes (bytes): Image data in byte format.

    Returns:
        Image: Grayscale PIL image ready for OCR.
    """
    image = Image.open(io.BytesIO(image_bytes))  # Load image from byte stream
    grayscale = image.convert("L")  # Convert to grayscale
    return grayscale

def ocr_image(image_bytes):
    """
    Perform OCR (Optical Character Recognition) on an image to extract text.

    Args:
        image_bytes (bytes): Image data in byte format.

    Returns:
        str: Extracted text from the image.
    """
    enhanced_image = enhance_image_for_ocr(image_bytes)  # Enhance the image
    ocr_text = pytesseract.image_to_string(enhanced_image)  # Extract text using OCR
    return ocr_text

def extract_images_and_ocr_from_page(page):
    """
    Extract images from a PDF page and perform OCR on each image.

    Args:
        page (fitz.Page): A PyMuPDF Page object.

    Returns:
        str: Combined OCR text extracted from all images on the page.
    """
    image_list = page.get_images(full=True)  # Get all images on the page
    ocr_results = []

    for img in image_list:
        xref = img[0]  # Image reference
        base_image = page.parent.extract_image(xref)  # Extract image data
        image_bytes = base_image["image"]  # Image bytes
        ocr_text = ocr_image(image_bytes)  # Perform OCR on the image
        ocr_results.append(ocr_text)  # Collect OCR text
    
    return "\n".join(ocr_results)  # Combine text from all images

def save_page_as_pdf(page, output_pdf_path):
    """
    Save a specific PDF page as a new single-page PDF.

    Args:
        page (fitz.Page): A PyMuPDF Page object.
        output_pdf_path (str): Path to save the new PDF.
    """
    pdf_writer = fitz.open()  # Create a new PDF writer object
    pdf_writer.insert_pdf(page.parent, from_page=page.number, to_page=page.number)  # Copy the page
    pdf_writer.save(output_pdf_path)  # Save the page as a new PDF
    pdf_writer.close()

def generate_output_pdf_filename(pdf_path):
    """
    Generate an output filename by truncating at the last underscore and appending '_BUILD'.

    Args:
        pdf_path (str): Original path to the input PDF.

    Returns:
        str: Generated output filename with '_BUILD.pdf' appended.
    """
    base_name = os.path.basename(pdf_path).replace('.pdf', '')  # Strip directory and extension
    truncated_name = base_name.rsplit('_', 1)[0]  # Truncate at the last underscore
    output_pdf_name = f"{truncated_name}_BUILD.pdf"
    return output_pdf_name

def find_and_save_page_with_text(pdf_path, search_text, output_folder, error_log_path):
    """
    Search for a specific text in a PDF, and save the page containing the text as a new PDF.
    - If the text is not found using normal text extraction, perform OCR on the page images.
    - If still not found, log the file to an error log.

    Args:
        pdf_path (str): Path to the input PDF file.
        search_text (str): Text to search for in the PDF.
        output_folder (str): Folder to save the resulting PDFs.
        error_log_path (str): Path to the error log file.
    """
    doc = fitz.open(pdf_path)  # Open the PDF
    text_found = False  # Flag to track if text is found
    pages_to_ocr = []  # List of pages to process with OCR if needed

    # Step 1: Search all pages using normal text extraction
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)  # Load each page
        extracted_text = page.get_text("text")  # Extract text

        if search_text.lower() in extracted_text.lower():
            # Save the page as a new PDF if text is found
            text_found = True
            output_pdf_filename = generate_output_pdf_filename(pdf_path)
            output_pdf_path = os.path.join(output_folder, output_pdf_filename)
            save_page_as_pdf(page, output_pdf_path)
            print(f"Text found and saved in {output_pdf_path}")
            break
        else:
            pages_to_ocr.append(page)  # Add page to the OCR list if text not found

    # Step 2: If text not found, perform OCR on pages with images
    if not text_found:
        for page in pages_to_ocr:
            print(f"Performing OCR on page {page.number + 1}...")
            ocr_text = extract_images_and_ocr_from_page(page)  # OCR the page images
            if search_text.lower() in ocr_text.lower():
                text_found = True
                output_pdf_filename = generate_output_pdf_filename(pdf_path)
                output_pdf_path = os.path.join(output_folder, output_pdf_filename)
                save_page_as_pdf(page, output_pdf_path)
                print(f"Text found via OCR and saved in {output_pdf_path}")
                break

    # Step 3: If text still not found, log the file to the error log
    if not text_found:
        with open(error_log_path, "a") as error_file:
            error_file.write(f"{pdf_path}\n")
        print(f"No text '{search_text}' found in {pdf_path}")

    doc.close()  # Close the PDF file

def process_pdfs_in_folder(folder_path, search_text, output_folder, error_log_path):
    """
    Process all PDFs in a folder to find pages containing specific text.

    Args:
        folder_path (str): Path to the folder containing PDF files.
        search_text (str): Text to search for in the PDFs.
        output_folder (str): Folder to save output PDFs.
        error_log_path (str): Path to the error log file.
    """
    os.makedirs(output_folder, exist_ok=True)  # Ensure output folder exists

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".pdf"):  # Process only PDF files
            pdf_path = os.path.join(folder_path, filename)
            print(f"Processing file: {filename}")
            find_and_save_page_with_text(pdf_path, search_text, output_folder, error_log_path)

# Example usage:
if __name__ == "__main__":
    # This is the main section of the script.
    # It defines the folder path, search text, output folder, and error log file paths.
    # Before running this script, make sure to install the required libraries:
    # pip install PyMuPDF pytesseract Pillow
    folder_path = "pdf"  # Folder containing PDF files
    search_text = "NULKA IGNITION UNIT SERIAL"  # Text to search for
    output_folder = "Build"  # Folder to save resulting PDFs
    error_log_path = "errors.txt"  # Path to error log file

    process_pdfs_in_folder(folder_path, search_text, output_folder, error_log_path)
