import pytest
from models import Invoice, LineItem, ValidationError, normalize_date, normalize_currency, normalize_text

def test_normalize_date():
    """Test date normalization with various formats."""
    assert normalize_date("2025-03-12") == "2025-03-12"
    assert normalize_date("12/03/2025") == "2025-03-12"
    # Note: In our implementation, 03/12/2025 is interpreted as MM/DD/YYYY
    # since both 03 and 12 are valid months, we default to DD/MM/YYYY format
    assert normalize_date("03/12/2025") == "2025-12-03"
    # Test with day > 12 to ensure it's interpreted as DD/MM/YYYY
    assert normalize_date("13/03/2025") == "2025-03-13"
    # Test with year first format
    assert normalize_date("2025/03/12") == "2025-03-12"

def test_normalize_currency():
    """Test currency value normalization."""
    assert normalize_currency("$1,234.56") == 1234.56
    assert normalize_currency("1234.56") == 1234.56
    assert normalize_currency(1234.56) == 1234.56
    assert normalize_currency("AUD 1,234.56") == 1234.56
    with pytest.raises(ValidationError):
        normalize_currency("invalid amount")

def test_normalize_text():
    """Test text normalization."""
    assert normalize_text("  Extra  Spaces  ") == "Extra Spaces"
    assert normalize_text("Multiple\nLines") == "Multiple Lines"
    with pytest.raises(ValidationError):
        normalize_text(None)

def test_line_item_validation():
    """Test LineItem validation."""
    # Valid line item
    line_item = LineItem(
        serviceDate="2025-03-12",
        serviceCode="SVC001",
        quantity=2.0,
        unitPrice=100.00,
        lineTotal=200.00,
        serviceDescription="Professional Services"
    )
    assert line_item.serviceDate == "2025-03-12"
    assert line_item.lineTotal == 200.00

    # Invalid quantity
    with pytest.raises(ValidationError):
        LineItem(
            serviceDate="2025-03-12",
            serviceCode="SVC001",
            quantity=0,  # Should be positive
            unitPrice=100.00,
            lineTotal=0.00,
            serviceDescription="Professional Services"
        )

    # Invalid line total
    with pytest.raises(ValidationError):
        LineItem(
            serviceDate="2025-03-12",
            serviceCode="SVC001",
            quantity=2.0,
            unitPrice=100.00,
            lineTotal=250.00,  # Should be 200.00
            serviceDescription="Professional Services"
        )

def test_invoice_validation():
    """Test Invoice validation."""
    # Valid invoice
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
    assert invoice.invoiceNumber == "INV-2025-001"
    assert invoice.totalAmount == 200.00

    # Invalid total amount
    with pytest.raises(ValidationError):
        Invoice(
            invoiceNumber="INV-2025-001",
            invoiceDate="2025-03-12",
            totalAmount=250.00,  # Doesn't match line items total
            vendor={"name": "ABC Company"},
            participant={"name": "John Doe"},
            lineItems=[line_item]
        )

    # Missing vendor name
    with pytest.raises(ValidationError):
        Invoice(
            invoiceNumber="INV-2025-001",
            invoiceDate="2025-03-12",
            totalAmount=200.00,
            vendor={},  # Missing name
            participant={"name": "John Doe"},
            lineItems=[line_item]
        )

def test_invoice_to_dict():
    """Test conversion of Invoice to dictionary."""
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
        dueDate="2025-04-11",
        totalAmount=200.00,
        vendor={"name": "ABC Company"},
        participant={"name": "John Doe"},
        lineItems=[line_item]
    )
    
    invoice_dict = invoice.to_dict()
    assert invoice_dict["invoiceNumber"] == "INV-2025-001"
    assert invoice_dict["totalAmount"] == 200.00
    assert len(invoice_dict["lineItems"]) == 1
    assert invoice_dict["lineItems"][0]["serviceCode"] == "SVC001"