import pytest
import os
import sys
import json

# Add project root to Python path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Configure pytest
def pytest_configure(config):
    """Configure pytest."""
    config.addinivalue_line(
        "markers",
        "unit: mark test as a unit test"
    )
    config.addinivalue_line(
        "markers",
        "integration: mark test as an integration test"
    )

@pytest.fixture(autouse=True)
def setup_logging():
    """Configure logging for tests."""
    import logging
    logging.basicConfig(level=logging.INFO)
    return logging.getLogger(__name__)

@pytest.fixture
def test_patterns():
    """Test patterns for invoice parsing."""
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
def parser(test_patterns, tmp_path):
    """Create InvoiceParser with test patterns."""
    from parse_invoice import InvoiceParser
    patterns_file = tmp_path / "test_patterns.json"
    with open(patterns_file, "w") as f:
        json.dump(test_patterns, f)
    return InvoiceParser(str(patterns_file))