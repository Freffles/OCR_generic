#!/usr/bin/python
"""
Test script for Google Sheets integration with real data.

This script demonstrates how to use the sheets_integration module
with real invoice data and actual Google Sheets.

Usage:
    python test_sheets_real.py

Requirements:
    - A client_secret.json file in the current directory
    - Google Sheets API enabled for the project
    - A Google Sheet named "NDIS-TEST" with worksheets "Invoices" and "output_invoice_data"
"""

import logging
import sys
import os
from datetime import datetime

from models import Invoice, LineItem
from sheets_integration import (
    get_sheets_client, 
    store_invoice, 
    store_invoices_batch,
    SheetsError,
    AuthError
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Find the client_secret file
def find_client_secret():
    """Find the client_secret file in the current directory."""
    for file_name in os.listdir('.'):
        if file_name.startswith('client_secret_') and file_name.endswith('.json'):
            logger.info(f"Found client secret file: {file_name}")
            return file_name
    return None

def create_sample_invoice():
    """Create a sample invoice for testing."""
    line_item = LineItem(
        serviceDate="2025-03-12",
        serviceCode="SVC001",
        quantity=2.0,
        unitPrice=100.00,
        lineTotal=200.00,
        serviceDescription="Professional Services"
    )
    
    invoice = Invoice(
        invoiceNumber=f"TEST-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
        invoiceDate="2025-03-12",
        totalAmount=200.00,
        vendor={"name": "ABC Company"},
        participant={"name": "John Doe"},
        lineItems=[line_item],
        dueDate="2025-04-11"
    )
    
    return invoice

def create_sample_invoices():
    """Create multiple sample invoices for batch testing."""
    # Invoice 1
    line_item1 = LineItem(
        serviceDate="2025-03-12",
        serviceCode="SVC001",
        quantity=2.0,
        unitPrice=100.00,
        lineTotal=200.00,
        serviceDescription="Professional Services"
    )
    
    invoice1 = Invoice(
        invoiceNumber=f"TEST-BATCH1-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
        invoiceDate="2025-03-12",
        totalAmount=200.00,
        vendor={"name": "ABC Company"},
        participant={"name": "John Doe"},
        lineItems=[line_item1],
        dueDate="2025-04-11"
    )
    
    # Invoice 2
    line_item2a = LineItem(
        serviceDate="2025-03-15",
        serviceCode="SVC002",
        quantity=1.0,
        unitPrice=150.00,
        lineTotal=150.00,
        serviceDescription="Consultation"
    )
    
    line_item2b = LineItem(
        serviceDate="2025-03-16",
        serviceCode="SVC003",
        quantity=3.0,
        unitPrice=50.00,
        lineTotal=150.00,
        serviceDescription="Support Hours"
    )
    
    invoice2 = Invoice(
        invoiceNumber=f"TEST-BATCH2-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
        invoiceDate="2025-03-15",
        totalAmount=300.00,
        vendor={"name": "XYZ Services"},
        participant={"name": "Jane Smith"},
        lineItems=[line_item2a, line_item2b],
        dueDate="2025-04-14"
    )
    
    return [invoice1, invoice2]

def test_single_invoice():
    """Test storing a single invoice."""
    try:
        # Get the Google Sheets client
        client = get_sheets_client(credentials_dir=".", token_file="token.json")
        
        # Create a sample invoice
        invoice = create_sample_invoice()
        
        # Store the invoice
        logger.info(f"Storing invoice {invoice.invoiceNumber}...")
        store_invoice(client, "NDIS-TEST", invoice)
        
        logger.info(f"Successfully stored invoice {invoice.invoiceNumber}")
        return True
    except AuthError as e:
        logger.error(f"Authentication error: {e}")
        return False
    except SheetsError as e:
        logger.error(f"Sheets error: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return False

def test_batch_invoices():
    """Test storing multiple invoices in batch."""
    try:
        # Get the Google Sheets client
        client = get_sheets_client(credentials_dir=".", token_file="token.json")
        
        # Create sample invoices
        invoices = create_sample_invoices()
        
        # Store the invoices
        logger.info(f"Storing {len(invoices)} invoices in batch...")
        result = store_invoices_batch(client, "NDIS-TEST", invoices)
        
        success_count, failure_count, failed_invoice_numbers = result
        
        logger.info(f"Successfully stored {success_count} invoices")
        if failure_count > 0:
            logger.warning(f"Failed to store {failure_count} invoices: {failed_invoice_numbers}")
        
        return success_count > 0
    except AuthError as e:
        logger.error(f"Authentication error: {e}")
        return False
    except SheetsError as e:
        logger.error(f"Sheets error: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return False

def main():
    """Main function."""
    logger.info("Testing Google Sheets integration with real data")
    
    # Check for client_secret file
    client_secret = find_client_secret()
    if not client_secret:
        logger.error("No client_secret file found in the current directory")
        logger.error("Please make sure you have a client_secret_*.json file in the current directory")
        return
    
    # Test single invoice
    logger.info("\n=== Testing Single Invoice Storage ===")
    single_result = test_single_invoice()
    
    # Test batch invoices
    logger.info("\n=== Testing Batch Invoice Storage ===")
    batch_result = test_batch_invoices()
    
    # Print summary
    logger.info("\n=== Test Summary ===")
    logger.info(f"Single Invoice Test: {'PASSED' if single_result else 'FAILED'}")
    logger.info(f"Batch Invoices Test: {'PASSED' if batch_result else 'FAILED'}")
    
    if single_result and batch_result:
        logger.info("All tests passed!")
    else:
        logger.warning("Some tests failed. Check the logs for details.")

if __name__ == "__main__":
    main()