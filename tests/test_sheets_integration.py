import os
import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime
import json

from models import Invoice, LineItem
import sheets_integration
from sheets_integration import (
    get_sheets_client, get_spreadsheet, get_worksheet,
    format_invoice_summary_row, format_invoice_detail_rows,
    append_to_sheet, store_invoice_summary, store_invoice_details,
    store_invoice, store_invoices_batch, SheetsError
)
from oauth_handler import AuthError

# Sample test data
@pytest.fixture
def sample_invoice():
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
        invoiceNumber="INV-2025-001",
        invoiceDate="2025-03-12",
        totalAmount=200.00,
        vendor={"name": "ABC Company"},
        participant={"name": "John Doe"},
        lineItems=[line_item],
        dueDate="2025-04-11"
    )
    
    return invoice

@pytest.fixture
def sample_invoices():
    """Create multiple sample invoices for batch testing."""
    invoices = []
    
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
        invoiceNumber="INV-2025-001",
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
        invoiceNumber="INV-2025-002",
        invoiceDate="2025-03-15",
        totalAmount=300.00,
        vendor={"name": "XYZ Services"},
        participant={"name": "Jane Smith"},
        lineItems=[line_item2a, line_item2b],
        dueDate="2025-04-14"
    )
    
    invoices.append(invoice1)
    invoices.append(invoice2)
    
    return invoices

@pytest.fixture
def mock_client():
    """Create a mock gspread client."""
    return MagicMock()

@pytest.fixture
def mock_spreadsheet():
    """Create a mock spreadsheet."""
    return MagicMock()

@pytest.fixture
def mock_worksheet():
    """Create a mock worksheet."""
    return MagicMock()

@pytest.fixture
def mock_api_error():
    """Create a proper mock for APIError."""
    error = MagicMock()
    error.__str__.return_value = "API error"
    return error

# Tests for helper functions
def test_format_invoice_summary_row(sample_invoice):
    """Test formatting an invoice as a summary row."""
    row = format_invoice_summary_row(sample_invoice)
    
    assert len(row) == 6
    assert row[0] == "INV-2025-001"
    assert row[1] == "2025-03-12"
    assert row[2] == "2025-04-11"
    assert row[3] == "ABC Company"
    assert row[4] == "John Doe"
    assert row[5] == 200.00

def test_format_invoice_detail_rows(sample_invoice):
    """Test formatting an invoice as detail rows."""
    rows = format_invoice_detail_rows(sample_invoice)
    
    assert len(rows) == 1  # One line item
    row = rows[0]
    assert len(row) == 10
    assert row[0] == "INV-2025-001"
    assert row[1] == "2025-03-12"
    assert row[2] == "ABC Company"
    assert row[3] == "John Doe"
    assert row[4] == "2025-03-12"
    assert row[5] == "SVC001"
    assert row[6] == "Professional Services"
    assert row[7] == 2.0
    assert row[8] == 100.00
    assert row[9] == 200.00

def test_format_invoice_detail_rows_no_line_items():
    """Test formatting an invoice with no line items."""
    invoice = Invoice(
        invoiceNumber="INV-2025-003",
        invoiceDate="2025-03-20",
        totalAmount=0.00,
        vendor={"name": "Test Vendor"},
        participant={"name": "Test Participant"},
        lineItems=[]
    )
    
    rows = format_invoice_detail_rows(invoice)
    
    assert len(rows) == 1  # Should create one row with empty line item fields
    row = rows[0]
    assert row[0] == "INV-2025-003"
    assert row[4] == ""  # Service date should be empty
    assert row[5] == ""  # Service code should be empty

# Tests for client and worksheet functions
@patch('sheets_integration.get_credentials')
def test_get_sheets_client_success(mock_get_credentials, mock_client):
    """Test successful creation of sheets client."""
    mock_get_credentials.return_value = MagicMock()
    
    with patch('gspread.authorize', return_value=mock_client):
        client = get_sheets_client()
        assert client == mock_client
        mock_get_credentials.assert_called_once()

@patch('sheets_integration.get_credentials')
def test_get_sheets_client_auth_error(mock_get_credentials):
    """Test handling of authentication error."""
    mock_get_credentials.side_effect = AuthError("Authentication failed")
    
    with pytest.raises(AuthError):
        get_sheets_client()

def test_get_spreadsheet_success(mock_client, mock_spreadsheet):
    """Test successful retrieval of spreadsheet."""
    mock_client.open.return_value = mock_spreadsheet
    
    spreadsheet = get_spreadsheet(mock_client, "Test Spreadsheet")
    assert spreadsheet == mock_spreadsheet
    mock_client.open.assert_called_once_with("Test Spreadsheet")

def test_get_spreadsheet_not_found(mock_client):
    """Test handling of spreadsheet not found."""
    from gspread.exceptions import SpreadsheetNotFound
    mock_client.open.side_effect = SpreadsheetNotFound("Spreadsheet not found")
    
    with pytest.raises(SheetsError):
        get_spreadsheet(mock_client, "Nonexistent Spreadsheet")

def test_get_worksheet_success(mock_spreadsheet, mock_worksheet):
    """Test successful retrieval of worksheet."""
    mock_spreadsheet.worksheet.return_value = mock_worksheet
    
    worksheet = get_worksheet(mock_spreadsheet, "Test Worksheet")
    assert worksheet == mock_worksheet
    mock_spreadsheet.worksheet.assert_called_once_with("Test Worksheet")

def test_get_worksheet_not_found(mock_spreadsheet):
    """Test handling of worksheet not found."""
    from gspread.exceptions import WorksheetNotFound
    mock_spreadsheet.worksheet.side_effect = WorksheetNotFound("Worksheet not found")
    
    with pytest.raises(SheetsError):
        get_worksheet(mock_spreadsheet, "Nonexistent Worksheet")

def test_append_to_sheet_success(mock_worksheet):
    """Test successful append to worksheet."""
    rows = [["A1", "B1"], ["A2", "B2"]]
    
    append_to_sheet(mock_worksheet, rows)
    mock_worksheet.append_rows.assert_called_once_with(rows)

def test_append_to_sheet_api_error_with_retry(mock_worksheet, mock_api_error):
    """Test retry logic for API errors."""
    from gspread.exceptions import APIError
    rows = [["A1", "B1"]]
    
    # First call raises APIError, second call succeeds
    mock_worksheet.append_rows.side_effect = [
        APIError(mock_api_error),
        None
    ]
    
    with patch('time.sleep') as mock_sleep:
        append_to_sheet(mock_worksheet, rows)
        assert mock_worksheet.append_rows.call_count == 2
        mock_sleep.assert_called_once()

def test_append_to_sheet_max_retries_exceeded(mock_worksheet, mock_api_error):
    """Test handling of max retries exceeded."""
    from gspread.exceptions import APIError
    rows = [["A1", "B1"]]
    
    # All calls raise APIError
    mock_worksheet.append_rows.side_effect = APIError(mock_api_error)
    
    with patch('time.sleep'), pytest.raises(SheetsError):
        append_to_sheet(mock_worksheet, rows)
        assert mock_worksheet.append_rows.call_count == 3  # MAX_RETRIES

# Tests for invoice storage functions
@patch('sheets_integration.get_spreadsheet')
@patch('sheets_integration.get_worksheet')
@patch('sheets_integration.append_to_sheet')
def test_store_invoice_summary(mock_append, mock_get_worksheet, mock_get_spreadsheet, 
                              mock_client, mock_spreadsheet, mock_worksheet, sample_invoice):
    """Test storing invoice summary."""
    mock_get_spreadsheet.return_value = mock_spreadsheet
    mock_get_worksheet.return_value = mock_worksheet
    
    store_invoice_summary(mock_client, "Test Spreadsheet", "Invoices", sample_invoice)
    
    mock_get_spreadsheet.assert_called_once_with(mock_client, "Test Spreadsheet")
    mock_get_worksheet.assert_called_once_with(mock_spreadsheet, "Invoices")
    mock_append.assert_called_once()
    # Verify the row format
    args = mock_append.call_args[0]
    assert args[0] == mock_worksheet
    assert len(args[1]) == 1  # One row
    assert len(args[1][0]) == 6  # Six columns

@patch('sheets_integration.get_spreadsheet')
@patch('sheets_integration.get_worksheet')
@patch('sheets_integration.append_to_sheet')
def test_store_invoice_details(mock_append, mock_get_worksheet, mock_get_spreadsheet, 
                              mock_client, mock_spreadsheet, mock_worksheet, sample_invoice):
    """Test storing invoice details."""
    mock_get_spreadsheet.return_value = mock_spreadsheet
    mock_get_worksheet.return_value = mock_worksheet
    
    store_invoice_details(mock_client, "Test Spreadsheet", "Details", sample_invoice)
    
    mock_get_spreadsheet.assert_called_once_with(mock_client, "Test Spreadsheet")
    mock_get_worksheet.assert_called_once_with(mock_spreadsheet, "Details")
    mock_append.assert_called_once()
    # Verify the row format
    args = mock_append.call_args[0]
    assert args[0] == mock_worksheet
    assert len(args[1]) == 1  # One line item
    assert len(args[1][0]) == 10  # Ten columns

@patch('sheets_integration.store_invoice_summary')
@patch('sheets_integration.store_invoice_details')
def test_store_invoice(mock_store_details, mock_store_summary, 
                      mock_client, sample_invoice):
    """Test storing complete invoice."""
    store_invoice(mock_client, "Test Spreadsheet", sample_invoice)
    
    mock_store_summary.assert_called_once_with(
        mock_client, "Test Spreadsheet", "Invoices", sample_invoice
    )
    mock_store_details.assert_called_once_with(
        mock_client, "Test Spreadsheet", "output_invoice_data", sample_invoice
    )

@patch('sheets_integration.get_spreadsheet')
@patch('sheets_integration.get_worksheet')
@patch('sheets_integration.append_to_sheet')
def test_store_invoices_batch(mock_append, mock_get_worksheet, mock_get_spreadsheet,
                             mock_client, mock_spreadsheet, mock_worksheet, sample_invoices):
    """Test batch storing of invoices."""
    mock_get_spreadsheet.return_value = mock_spreadsheet
    mock_get_worksheet.return_value = mock_worksheet
    
    result = store_invoices_batch(mock_client, "Test Spreadsheet", sample_invoices)
    
    assert result[0] == 2  # 2 successful
    assert result[1] == 0  # 0 failed
    assert result[2] == []  # No failed invoice numbers
    
    mock_get_spreadsheet.assert_called_once_with(mock_client, "Test Spreadsheet")
    assert mock_get_worksheet.call_count == 2  # Once for summary, once for details
    assert mock_append.call_count == 2  # Once for summary rows, once for detail rows

@patch('sheets_integration.get_spreadsheet')
@patch('sheets_integration.get_worksheet')
@patch('sheets_integration.append_to_sheet')
def test_store_invoices_batch_partial_failure(mock_append, mock_get_worksheet, mock_get_spreadsheet,
                                            mock_client, mock_spreadsheet, mock_worksheet, sample_invoices):
    """Test batch storing with partial failure."""
    mock_get_spreadsheet.return_value = mock_spreadsheet
    mock_get_worksheet.return_value = mock_worksheet
    
    # Make the first append succeed but the second fail
    mock_append.side_effect = [None, SheetsError("Failed to append detail rows")]
    
    with pytest.raises(SheetsError):
        store_invoices_batch(mock_client, "Test Spreadsheet", sample_invoices)
    
    assert mock_append.call_count == 2

# Integration-style tests (still using mocks)
@patch('sheets_integration.get_credentials')
def test_full_invoice_storage_flow(mock_get_credentials, sample_invoice):
    """Test the full flow of storing an invoice."""
    # Setup all the mocks
    mock_creds = MagicMock()
    mock_get_credentials.return_value = mock_creds
    
    mock_client = MagicMock()
    mock_spreadsheet = MagicMock()
    mock_summary_ws = MagicMock()
    mock_details_ws = MagicMock()
    
    with patch('gspread.authorize', return_value=mock_client) as mock_authorize:
        with patch.object(mock_client, 'open', return_value=mock_spreadsheet):
            with patch.object(mock_spreadsheet, 'worksheet') as mock_worksheet:
                # Return different worksheets based on name
                mock_worksheet.side_effect = lambda name: mock_summary_ws if name == "Invoices" else mock_details_ws
                
                # Call the function
                store_invoice(
                    get_sheets_client(),
                    "Test Spreadsheet",
                    sample_invoice
                )
                
                # Verify the flow
                mock_get_credentials.assert_called_once()
                mock_authorize.assert_called_once_with(mock_creds)
                mock_client.open.assert_called_with("Test Spreadsheet")
                assert mock_worksheet.call_count == 2
                assert mock_summary_ws.append_rows.call_count == 1
                assert mock_details_ws.append_rows.call_count == 1