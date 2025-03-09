# parse_invoice.py
import re
from models import Invoice, LineItem

def parse_invoice_text(raw_text: str) -> Invoice:
    # Sample regex extractions; you'll need to adapt these for your invoice formats.
    invoice_number = re.search(r"Invoice Number[:\s]*([A-Z0-9\-_]+)", raw_text)
    invoice_date = re.search(r"Invoice Date[:\s]*([\d/]+)", raw_text)
    due_date = re.search(r"Due Date[:\s]*([\d/]+)", raw_text)
    total_amount = re.search(r"TOTAL\s*(AUD)?\s*\$?([\d.,]+)", raw_text)
    
    # Dummy line item extraction (customize as needed)
    line_items = []
    # For instance, use a regex to extract line item details here
    
    return Invoice(
        invoiceNumber=invoice_number.group(1) if invoice_number else "",
        invoiceDate=invoice_date.group(1) if invoice_date else "",
        dueDate=due_date.group(1) if due_date else "",
        totalAmount=float(total_amount.group(2).replace(',', '')) if total_amount else 0,
        vendor={"name": extract_vendor_name(raw_text)},
        participant={"name": extract_participant_name(raw_text)},
        lineItems=line_items
    )

def extract_vendor_name(text: str) -> str:
    # Example extraction logic for vendor name
    match = re.search(r"(?i)(Applied Communication Skills Pty Ltd|Waves of Harmony Pty Ltd|APLUS DISABILITY SERVICE GROUP PTY LTD)", text)
    return match.group(0) if match else ""

def extract_participant_name(text: str) -> str:
    # Example extraction logic for participant name
    match = re.search(r"Provided To:\s*([A-Za-z\s]+)", text)
    return match.group(1).strip() if match else ""
