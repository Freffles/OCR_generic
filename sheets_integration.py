import os
import logging
import time
from typing import List, Dict, Any, Optional, Union
import gspread
from gspread.exceptions import APIError, SpreadsheetNotFound, WorksheetNotFound
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from models import Invoice, LineItem
from oauth_handler import get_credentials, AuthError

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Constants
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds

class SheetsError(Exception):
    """Exception raised for Google Sheets integration errors."""
    pass

def get_sheets_client(credentials_dir=None, token_file=None):
    """
    Get an authorized Google Sheets client.
    
    Args:
        credentials_dir: Directory containing the client_secret file
        token_file: Path to the token file (relative to credentials_dir)
        
    Returns:
        gspread client object
        
    Raises:
        AuthError: If authentication fails
        SheetsError: If client creation fails
    """
    try:
        # Get credentials using our OAuth handler
        creds = get_credentials(credentials_dir, token_file)
        
        # Create and return the gspread client
        client = gspread.authorize(creds)
        logger.info("Successfully created Google Sheets client")
        return client
    except AuthError as e:
        logger.error(f"Authentication failed: {e}")
        raise
    except Exception as e:
        logger.error(f"Failed to create Sheets client: {e}")
        raise SheetsError(f"Failed to create Sheets client: {e}")

def get_spreadsheet(client, spreadsheet_name: str):
    """
    Get a spreadsheet by name with retry logic.
    
    Args:
        client: Authorized gspread client
        spreadsheet_name: Name of the spreadsheet
        
    Returns:
        gspread Spreadsheet object
        
    Raises:
        SheetsError: If spreadsheet cannot be accessed after retries
    """
    for attempt in range(MAX_RETRIES):
        try:
            spreadsheet = client.open(spreadsheet_name)
            return spreadsheet
        except SpreadsheetNotFound:
            logger.error(f"Spreadsheet '{spreadsheet_name}' not found")
            raise SheetsError(f"Spreadsheet '{spreadsheet_name}' not found")
        except APIError as e:
            if attempt < MAX_RETRIES - 1:
                logger.warning(f"API error accessing spreadsheet (attempt {attempt+1}): {e}")
                time.sleep(RETRY_DELAY)
            else:
                logger.error(f"Failed to access spreadsheet after {MAX_RETRIES} attempts: {e}")
                raise SheetsError(f"Failed to access spreadsheet: {e}")
        except Exception as e:
            logger.error(f"Unexpected error accessing spreadsheet: {e}")
            raise SheetsError(f"Unexpected error accessing spreadsheet: {e}")

def get_worksheet(spreadsheet, worksheet_name: str):
    """
    Get a worksheet by name with retry logic.
    
    Args:
        spreadsheet: gspread Spreadsheet object
        worksheet_name: Name of the worksheet
        
    Returns:
        gspread Worksheet object
        
    Raises:
        SheetsError: If worksheet cannot be accessed after retries
    """
    for attempt in range(MAX_RETRIES):
        try:
            worksheet = spreadsheet.worksheet(worksheet_name)
            return worksheet
        except WorksheetNotFound:
            logger.error(f"Worksheet '{worksheet_name}' not found")
            raise SheetsError(f"Worksheet '{worksheet_name}' not found")
        except APIError as e:
            if attempt < MAX_RETRIES - 1:
                logger.warning(f"API error accessing worksheet (attempt {attempt+1}): {e}")
                time.sleep(RETRY_DELAY)
            else:
                logger.error(f"Failed to access worksheet after {MAX_RETRIES} attempts: {e}")
                raise SheetsError(f"Failed to access worksheet: {e}")
        except Exception as e:
            logger.error(f"Unexpected error accessing worksheet: {e}")
            raise SheetsError(f"Unexpected error accessing worksheet: {e}")

def format_invoice_summary_row(invoice: Invoice) -> List[Any]:
    """
    Format an invoice as a summary row for the 'Invoices' sheet.
    
    Args:
        invoice: Invoice object
        
    Returns:
        List of values for a single row
    """
    # Format: [Invoice Number, Date, Due Date, Vendor, Participant, Total Amount]
    return [
        invoice.invoiceNumber,
        invoice.invoiceDate,
        invoice.dueDate if invoice.dueDate else "",
        invoice.vendor.get("name", ""),
        invoice.participant.get("name", ""),
        invoice.totalAmount
    ]

def format_invoice_detail_rows(invoice: Invoice) -> List[List[Any]]:
    """
    Format an invoice as multiple detail rows for the 'output_invoice_data' sheet.
    Each line item gets its own row with invoice header information.
    
    Args:
        invoice: Invoice object
        
    Returns:
        List of rows, each containing values for a line item
    """
    rows = []
    
    for item in invoice.lineItems:
        # Format: [Invoice Number, Date, Vendor, Participant, Service Date, 
        #          Service Code, Description, Quantity, Unit Price, Line Total]
        row = [
            invoice.invoiceNumber,
            invoice.invoiceDate,
            invoice.vendor.get("name", ""),
            invoice.participant.get("name", ""),
            item.serviceDate,
            item.serviceCode,
            item.serviceDescription,
            item.quantity,
            item.unitPrice,
            item.lineTotal
        ]
        rows.append(row)
    
    # If no line items, create a single row with invoice info and empty line item fields
    if not rows:
        row = [
            invoice.invoiceNumber,
            invoice.invoiceDate,
            invoice.vendor.get("name", ""),
            invoice.participant.get("name", ""),
            "", "", "", "", "", ""
        ]
        rows.append(row)
    
    return rows

def append_to_sheet(worksheet, rows: List[List[Any]]):
    """
    Append rows to a worksheet with retry logic.
    
    Args:
        worksheet: gspread Worksheet object
        rows: List of rows to append
        
    Raises:
        SheetsError: If append operation fails after retries
    """
    if not rows:
        logger.warning("No rows to append")
        return
    
    for attempt in range(MAX_RETRIES):
        try:
            worksheet.append_rows(rows)
            logger.info(f"Successfully appended {len(rows)} rows to worksheet")
            return
        except APIError as e:
            if attempt < MAX_RETRIES - 1:
                logger.warning(f"API error appending rows (attempt {attempt+1}): {e}")
                time.sleep(RETRY_DELAY)
            else:
                logger.error(f"Failed to append rows after {MAX_RETRIES} attempts: {e}")
                raise SheetsError(f"Failed to append rows: {e}")
        except Exception as e:
            logger.error(f"Unexpected error appending rows: {e}")
            raise SheetsError(f"Unexpected error appending rows: {e}")

def store_invoice_summary(client, spreadsheet_name: str, worksheet_name: str, invoice: Invoice):
    """
    Store an invoice summary in the specified spreadsheet and worksheet.
    
    Args:
        client: Authorized gspread client
        spreadsheet_name: Name of the spreadsheet
        worksheet_name: Name of the worksheet
        invoice: Invoice object to store
        
    Raises:
        SheetsError: If operation fails
    """
    try:
        spreadsheet = get_spreadsheet(client, spreadsheet_name)
        worksheet = get_worksheet(spreadsheet, worksheet_name)
        
        row = format_invoice_summary_row(invoice)
        append_to_sheet(worksheet, [row])
        
        logger.info(f"Successfully stored invoice {invoice.invoiceNumber} summary")
    except (SheetsError, AuthError) as e:
        # Re-raise these exceptions as they're already properly formatted
        raise
    except Exception as e:
        logger.error(f"Failed to store invoice summary: {e}")
        raise SheetsError(f"Failed to store invoice summary: {e}")

def store_invoice_details(client, spreadsheet_name: str, worksheet_name: str, invoice: Invoice):
    """
    Store invoice details (line items) in the specified spreadsheet and worksheet.
    
    Args:
        client: Authorized gspread client
        spreadsheet_name: Name of the spreadsheet
        worksheet_name: Name of the worksheet
        invoice: Invoice object to store
        
    Raises:
        SheetsError: If operation fails
    """
    try:
        spreadsheet = get_spreadsheet(client, spreadsheet_name)
        worksheet = get_worksheet(spreadsheet, worksheet_name)
        
        rows = format_invoice_detail_rows(invoice)
        append_to_sheet(worksheet, rows)
        
        logger.info(f"Successfully stored invoice {invoice.invoiceNumber} details with {len(rows)} line items")
    except (SheetsError, AuthError) as e:
        # Re-raise these exceptions as they're already properly formatted
        raise
    except Exception as e:
        logger.error(f"Failed to store invoice details: {e}")
        raise SheetsError(f"Failed to store invoice details: {e}")

def store_invoice(client, spreadsheet_name: str, invoice: Invoice, 
                 summary_worksheet: str = "Invoices", 
                 details_worksheet: str = "output_invoice_data"):
    """
    Store an invoice in both summary and detail formats.
    
    Args:
        client: Authorized gspread client
        spreadsheet_name: Name of the spreadsheet
        invoice: Invoice object to store
        summary_worksheet: Name of the worksheet for summary data
        details_worksheet: Name of the worksheet for detailed data
        
    Raises:
        SheetsError: If operation fails
    """
    try:
        # Store summary
        store_invoice_summary(client, spreadsheet_name, summary_worksheet, invoice)
        
        # Store details
        store_invoice_details(client, spreadsheet_name, details_worksheet, invoice)
        
        logger.info(f"Successfully stored invoice {invoice.invoiceNumber} in both formats")
    except (SheetsError, AuthError) as e:
        # Re-raise these exceptions as they're already properly formatted
        raise
    except Exception as e:
        logger.error(f"Failed to store invoice: {e}")
        raise SheetsError(f"Failed to store invoice: {e}")

def store_invoices_batch(client, spreadsheet_name: str, invoices: List[Invoice],
                        summary_worksheet: str = "Invoices", 
                        details_worksheet: str = "output_invoice_data"):
    """
    Store multiple invoices in batch.
    
    Args:
        client: Authorized gspread client
        spreadsheet_name: Name of the spreadsheet
        invoices: List of Invoice objects to store
        summary_worksheet: Name of the worksheet for summary data
        details_worksheet: Name of the worksheet for detailed data
        
    Returns:
        Tuple of (success_count, failure_count, failed_invoice_numbers)
        
    Raises:
        SheetsError: If all operations fail
    """
    if not invoices:
        logger.warning("No invoices to store")
        return (0, 0, [])
    
    success_count = 0
    failure_count = 0
    failed_invoice_numbers = []
    
    try:
        spreadsheet = get_spreadsheet(client, spreadsheet_name)
        summary_ws = get_worksheet(spreadsheet, summary_worksheet)
        details_ws = get_worksheet(spreadsheet, details_worksheet)
        
        # Prepare all summary rows
        summary_rows = []
        for invoice in invoices:
            try:
                row = format_invoice_summary_row(invoice)
                summary_rows.append(row)
            except Exception as e:
                logger.error(f"Failed to format invoice {invoice.invoiceNumber} summary: {e}")
                failure_count += 1
                failed_invoice_numbers.append(invoice.invoiceNumber)
        
        # Append all summary rows in one batch
        if summary_rows:
            append_to_sheet(summary_ws, summary_rows)
            logger.info(f"Successfully stored {len(summary_rows)} invoice summaries")
        
        # Prepare all detail rows
        all_detail_rows = []
        for invoice in invoices:
            if invoice.invoiceNumber in failed_invoice_numbers:
                continue  # Skip already failed invoices
                
            try:
                detail_rows = format_invoice_detail_rows(invoice)
                all_detail_rows.extend(detail_rows)
                success_count += 1
            except Exception as e:
                logger.error(f"Failed to format invoice {invoice.invoiceNumber} details: {e}")
                failure_count += 1
                failed_invoice_numbers.append(invoice.invoiceNumber)
        
        # Append all detail rows in one batch
        if all_detail_rows:
            append_to_sheet(details_ws, all_detail_rows)
            logger.info(f"Successfully stored {len(all_detail_rows)} invoice detail rows")
        
        if failure_count == len(invoices):
            raise SheetsError(f"All {len(invoices)} invoices failed to store")
            
        return (success_count, failure_count, failed_invoice_numbers)
        
    except (SheetsError, AuthError) as e:
        # Re-raise these exceptions as they're already properly formatted
        raise
    except Exception as e:
        logger.error(f"Failed to store invoices batch: {e}")
        raise SheetsError(f"Failed to store invoices batch: {e}")
