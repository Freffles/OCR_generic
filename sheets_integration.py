# sheets_integration.py
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def get_sheet(spreadsheet_name: str, worksheet_name: str):
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('path/to/credentials.json', scope)
    client = gspread.authorize(creds)
    spreadsheet = client.open(spreadsheet_name)
    worksheet = spreadsheet.worksheet(worksheet_name)
    return worksheet

def append_invoice_row(worksheet, invoice):
    # Convert your Invoice object into a row format. Adjust fields as needed.
    # For example, flatten the invoice data:
    row = [
        invoice.invoiceNumber,
        invoice.invoiceDate,
        invoice.dueDate,
        invoice.totalAmount,
        invoice.vendor.get("name"),
        invoice.participant.get("name")
        # If you want to include line item details, you might join them as a string or handle them separately.
    ]
    worksheet.append_row(row)
