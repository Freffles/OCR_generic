import pytest
import json
from parse_invoice import InvoiceParser, InvoiceParsingError
from models import Invoice, LineItem

@pytest.fixture
def sample_patterns():
    """Sample patterns for testing."""
    return {
        "invoice_types": {
            "test_vendor": {
                "name": "Test Vendor Pty Ltd",
                "patterns": {
                    "invoice_number": "Invoice Number[:\\s]*([A-Z0-9\\-_]+)",
                    "invoice_date": "Invoice Date[:\\s]*(\\d{1,2}/\\d{1,2}/\\d{4})",
                    "due_date": "Due Date[:\\s]*(\\d{1,2}/\\d{1,2}/\\d{4})",
                    "total_amount": "TOTAL[\\s\\n]*\\$?([\\d.,]+)",
                    "participant": "Provided To:\\s*([A-Za-z\\s]+?)(?=\\s*$|\\s*Description)",
                    "line_items": {
                        "table_start": "Description\\s+Quantity\\s+Unit Price\\s+Amount",
                        "row": "([^\\n]+?)\\s+(\\d+(?:\\.\\d+)?)\\s+\\$?([\\d.,]+)\\s+\\$?([\\d.,]+)",
                        "table_end": "Sub\\s*Total|TOTAL"
                    }
                }
            },
            "generic": {
                "name": "Generic Invoice",
                "patterns": {
                    "invoice_number": "(?i)Invoice\\s*(?:No|Number|#)?[:\\s]*([A-Z0-9\\-_]+)",
                    "invoice_date": "(?i)(?:Invoice\\s*)?Date[:\\s]*(\\d{1,2}[/\\-]\\d{1,2}[/\\-]\\d{4})",
                    "due_date": "(?i)(?:Due|Payment\\s*Due)[:\\s]*(\\d{1,2}[/\\-]\\d{1,2}[/\\-]\\d{4})",
                    "total_amount": "(?i)(?:Total|Amount\\s*Due|Invoice\\s*Total)[\\s\\n]*\\$?([\\d.,]+)",
                    "participant": "(?i)(?:Bill\\s*To|Client|Customer|Provided\\s*To)[:\\s]*([A-Za-z\\s]+?)(?=\\s*$|\\s*(?:Description|Service|Item))",
                    "line_items": {
                        "table_start": "(?i)(?:Description|Service|Item)\\s+(?:Qty|Quantity)\\s+(?:Rate|Price|Unit\\s*Price)\\s+(?:Amount|Total)",
                        "row": "([^\\n]+?)\\s+(\\d+(?:\\.\\d+)?)\\s+\\$?([\\d.,]+)\\s+\\$?([\\d.,]+)",
                        "table_end": "(?i)(?:Sub\\s*Total|Total|Invoice\\s*Total)"
                    }
                }
            }
        }
    }

@pytest.fixture
def sample_invoice_text():
    """Sample invoice text for testing."""
    return """
    Test Vendor Pty Ltd
    
    Invoice Number: INV-2025-001
    Invoice Date: 12/03/2025
    Due Date: 11/04/2025
    
    Provided To: John Smith
    
    Description                 Quantity    Unit Price    Amount
    Professional Services      2           $100.00       $200.00
    
    TOTAL                                              $200.00
    """

@pytest.fixture
def parser(sample_patterns, tmp_path):
    """Create InvoiceParser with sample patterns."""
    patterns_file = tmp_path / "test_patterns.json"
    with open(patterns_file, "w") as f:
        json.dump(sample_patterns, f)
    return InvoiceParser(str(patterns_file))

def test_detect_invoice_type(parser, sample_invoice_text):
    """Test invoice type detection."""
    invoice_type, patterns = parser.detect_invoice_type(sample_invoice_text)
    assert invoice_type == "test_vendor"
    assert patterns["invoice_number"] == "Invoice Number[:\\s]*([A-Z0-9\\-_]+)"

def test_extract_field(parser, sample_invoice_text):
    """Test field extraction."""
    _, patterns = parser.detect_invoice_type(sample_invoice_text)
    
    invoice_number = parser.extract_field(
        sample_invoice_text,
        patterns["invoice_number"],
        "invoice_number"
    )
    assert invoice_number == "INV-2025-001"

    total_amount = parser.extract_field(
        sample_invoice_text,
        patterns["total_amount"],
        "total_amount"
    )
    assert total_amount == "200.00"

def test_extract_line_items(parser, sample_invoice_text):
    """Test line item extraction."""
    _, patterns = parser.detect_invoice_type(sample_invoice_text)
    line_items = parser.extract_line_items(sample_invoice_text, patterns)
    
    assert len(line_items) == 1
    assert line_items[0].serviceDescription == "Professional Services"
    assert line_items[0].quantity == 2.0
    assert line_items[0].unitPrice == 100.00
    assert line_items[0].lineTotal == 200.00

def test_parse_invoice(parser, sample_invoice_text):
    """Test complete invoice parsing."""
    invoice = parser.parse_invoice(sample_invoice_text)
    
    assert isinstance(invoice, Invoice)
    assert invoice.invoiceNumber == "INV-2025-001"
    assert invoice.invoiceDate == "2025-03-12"
    assert invoice.dueDate == "2025-04-11"
    assert invoice.totalAmount == 200.00
    assert invoice.vendor["name"] == "Test Vendor Pty Ltd"
    assert invoice.participant["name"] == "John Smith"
    assert len(invoice.lineItems) == 1

def test_parse_invoice_missing_required_field(parser):
    """Test parsing with missing required field."""
    invalid_text = """
    Test Vendor Pty Ltd
    
    Invoice Date: 12/03/2025
    Due Date: 11/04/2025
    """
    with pytest.raises(InvoiceParsingError):
        parser.parse_invoice(invalid_text)

def test_parse_invoice_invalid_amount(parser):
    """Test parsing with invalid amount format."""
    invalid_text = """
    Test Vendor Pty Ltd
    
    Invoice Number: INV-2025-001
    Invoice Date: 12/03/2025
    
    TOTAL invalid
    """
    with pytest.raises(InvoiceParsingError):
        parser.parse_invoice(invalid_text)

def test_extract_table_section(parser, sample_invoice_text):
    """Test table section extraction."""
    _, patterns = parser.detect_invoice_type(sample_invoice_text)
    table_text = parser._extract_table_section(sample_invoice_text, patterns["line_items"])
    
    assert "Professional Services" in table_text
    assert "2" in table_text
    assert "$100.00" in table_text
    assert "$200.00" in table_text

def test_fallback_to_generic_patterns(parser):
    """Test fallback to generic patterns when vendor not recognized."""
    unknown_vendor_text = """
    Unknown Vendor Ltd
    
    Invoice #: INV-2025-001
    Date: 12/03/2025
    Total Due: $200.00
    """
    invoice_type, patterns = parser.detect_invoice_type(unknown_vendor_text)
    assert invoice_type == "generic"
    assert "invoice_number" in patterns