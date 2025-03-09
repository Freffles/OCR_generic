# process_invoices.py
import os
import json
from extract_text import extract_text_from_pdf
from parse_invoice import parse_invoice_text
from sheets_integration import get_sheet, append_invoice_row

def process_single_invoice(file_path: str, worksheet):
    raw_text = extract_text_from_pdf(file_path)
    invoice = parse_invoice_text(raw_text)
    append_invoice_row(worksheet, invoice)
    print(f"Processed: {file_path}")

def process_folder(folder_path: str, worksheet):
    for filename in os.listdir(folder_path):
        if filename.lower().endswith('.pdf'):
            file_path = os.path.join(folder_path, filename)
            try:
                process_single_invoice(file_path, worksheet)
            except Exception as e:
                print(f"Error processing {file_path}: {e}")

if __name__ == "__main__":
    # Setup your Google Sheet connection
    worksheet = get_sheet("Your Spreadsheet Name", "Sheet1")
    
    # Process a single invoice:
    # process_single_invoice("path/to/single/invoice.pdf", worksheet)
    
    # Or process all invoices in a folder:
    process_folder("path/to/invoices_folder", worksheet)
