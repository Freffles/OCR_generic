# OCR Generic Project

This project contains a collection of Python scripts for OCR and PDF processing.

## Scripts

### csv_add_dest.py
This script inserts a "Source" column into each CSV file located in the specified folder. The value for the "Source" column is derived from the original filename of the CSV file.

Functions:
*   **N/A**

### csv_cleanup_next_step.py
This script processes CSV files in a specified folder to remove unnecessary rows from the beginning of each file. It searches for a row starting with 'Lvl' or 'Structure Level' and keeps only the rows from that point onwards. Files where the search string is not found are logged in an error file.

Functions:
*   **N/A**

### csv_consolidate.py
This script consolidates all CSV files located in the specified folder into a single master CSV file.

Functions:
*   **N/A**

### csv_from_xls.py
This script converts Excel files (with .xlsx extension) listed in the 'output_file.csv' into individual CSV files and saves them in a specified directory.

Functions:
*   **N/A**

### csv_xslsx_files.py
This script finds all the Excel files (with .xlsx extension) within a specified folder and its sub-folders. It then extracts the filename and creation date of each Excel file and writes this information to a CSV file named 'output_file.csv'.

Functions:
*   **N/A**

### ocr_pg1.py
This module extracts dates from PDF files by performing OCR on the first page. It uses PyMuPDF to open the PDF and pytesseract to perform OCR on images. The extracted dates are saved to a CSV file, and the OCR text for files without dates is saved to a debug file.

Functions:
*   **ocr_image(image_bytes)**: Perform OCR (Optical Character Recognition) on an image.
*   **extract_and_ocr_images_from_first_page(pdf_path)**: Extract and perform OCR on all images found on the first page of a PDF.
*   **identify_and_normalize_date(date_str)**: Identify and normalize a date string to 'DD-MM-YYYY' format.
*   **extract_date_from_text(text)**: Extract the first date occurrence from the OCR text.
*   **process_pdfs_and_generate_csv(folder_path, csv_file, debug_text_file)**: Process all PDFs in a folder to extract dates from images on the first page.

### speedbumps.py
This script reads data from an Excel file, adds a date column, and converts the data to a Markdown table, which is then saved to a text file.

Functions:
*   **N/A**

### ocr_srch.py
This module provides functions for extracting text from PDF files using OCR. It includes functions for enhancing images, performing OCR, and saving the extracted text.

Functions:
*   **enhance_image_for_ocr(image_bytes)**: Enhance an image for better OCR results by converting it to grayscale.
*   **ocr_image(image_bytes)**: Perform OCR (Optical Character Recognition) on an image to extract text.
*   **extract_images_and_ocr_from_page(page)**: Extract images from a PDF page and perform OCR on each image.
*   **save_page_as_pdf(page, output_pdf_path)**: Save a specific PDF page as a new single-page PDF.
*   **generate_output_pdf_filename(pdf_path)**: Generate an output filename by truncating at the last underscore and appending '_BUILD'.
*   **find_and_save_page_with_text(pdf_path, search_text, output_folder, error_log_path)**: Search for a specific text in a PDF, and save the page containing the text as a new PDF.
*   **process_pdfs_in_folder(folder_path, search_text, output_folder, error_log_path)**: Process all PDFs in a folder to find pages containing specific text.

### ocr_wo_extract_all.py
This module extracts text and dates from PDF files. It uses PyMuPDF for PDF processing and pytesseract for OCR when needed. The extracted data is saved to a CSV file.

Functions:
*   **extract_text_from_first_page(pdf_path)**: Extract text from the first page of a PDF.
*   **save_text_to_file(pdf_path, text, debug_file)**: Save the extracted text to a debug output file for inspection.
*   **normalize_date(date_str)**: Normalize a date string into 'DD-MM-YYYY' format.
*   **extract_date_from_text(text)**: Extract the first occurrence of a date string from the text.
*   **process_pdfs_and_generate_csv(folder_path, csv_file, debug_file)**: Process all PDF files in a folder.

### ocr_pdf_extract_pypdf2.py
This module extracts text and dates from PDF files using PyPDF2 and PyMuPDF. It falls back to OCR if direct text extraction fails. The extracted data is saved to a CSV file.

Functions:
*   **extract_text_from_first_page(pdf_path)**: Extract text from the first page of a PDF using PyPDF2.
*   **enhance_image_for_ocr(image)**: Enhance an image for better OCR results by converting to grayscale and reducing noise.
*   **extract_text_with_ocr(pdf_path)**: Perform OCR on the first page of a PDF to extract text.
*   **save_text_to_file(pdf_path, text, debug_file)**: Save extracted text from a PDF to a debug output file.
*   **normalize_date(date_str)**: Normalize a date string to 'DD-MM-YYYY' format.
*   **extract_date_from_text(text)**: Extract the first 'Date Printed' occurrence from the text.
*   **process_pdfs_and_generate_csv(folder_path, csv_file, debug_file)**: Process all PDFs in a folder, extract text, find dates, and write results to a CSV file.

### pdf_properties.py
This module extracts properties from PDF files, including metadata, page count, and image information. It can process all PDF files in a specified folder and write the extracted properties to a CSV file.

Functions:
*   **extract_pdf_properties(pdf_path)**: Extract metadata, page count, and image information from a PDF file.
*   **process_pdfs_in_folder(folder_path)**: Process all PDF files in a specified folder and extract their properties.
*   **write_properties_to_csv(pdf_properties_list, csv_filename)**: Write the extracted PDF properties to a CSV file.