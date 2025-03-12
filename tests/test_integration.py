import pytest
from models import Invoice, LineItem
from parse_invoice import InvoiceParser

@pytest.fixture
def sample_invoice_texts():
    """Sample invoice texts for different vendors."""
    return {
        "applied_communication": """
        Applied Communication Skills Pty Ltd

        Invoice Number: ACS-2025-001
        Invoice Date: 12/03/2025
        Due Date: 11/04/2025

        Provided To: John Smith

        Description                 Quantity    Unit Price    Amount
        Professional Services      2           $100.00       $200.00
        Training Session          1           $150.00       $150.00

        TOTAL                                              $350.00
        """,
        
        "waves_of_harmony": """
        Waves of Harmony Pty Ltd

        Invoice #: WOH-2025-001
        Date: 12/03/2025
        Due: 11/04/2025

        Bill To: Jane Doe

        Service                    Qty         Rate         Amount
        Music Therapy             3           $80.00       $240.00
        Equipment Rental          1           $50.00       $50.00

        Total Due                                         $290.00
        """,
        
        "aplus_disability": """
        APLUS DISABILITY SERVICE GROUP PTY LTD

        Invoice No: APD-2025-001
        Date: 12/03/2025
        Payment Due: 11/04/2025

        Client: Bob Wilson

        Service Description        Qty         Price        Total
        Support Coordination      4           $95.00       $380.00
        Transport Service        2           $40.00       $80.00

        Invoice Total                                     $460.00
        """
    }

def test_parse_applied_communication_invoice(sample_invoice_texts):
    """Test parsing Applied Communication Skills invoice."""
    parser = InvoiceParser()
    invoice = parser.parse_invoice(sample_invoice_texts["applied_communication"])
    
    assert invoice.invoiceNumber == "ACS-2025-001"
    assert invoice.invoiceDate == "2025-03-12"
    assert invoice.dueDate == "2025-04-11"
    assert invoice.totalAmount == 350.00
    assert invoice.vendor["name"] == "Applied Communication Skills Pty Ltd"
    assert invoice.participant["name"] == "John Smith"
    assert len(invoice.lineItems) == 2
    
    # Check first line item
    assert invoice.lineItems[0].serviceDescription == "Professional Services"
    assert invoice.lineItems[0].quantity == 2.0
    assert invoice.lineItems[0].unitPrice == 100.00
    assert invoice.lineItems[0].lineTotal == 200.00
    
    # Check second line item
    assert invoice.lineItems[1].serviceDescription == "Training Session"
    assert invoice.lineItems[1].quantity == 1.0
    assert invoice.lineItems[1].unitPrice == 150.00
    assert invoice.lineItems[1].lineTotal == 150.00

def test_parse_waves_of_harmony_invoice(sample_invoice_texts):
    """Test parsing Waves of Harmony invoice."""
    parser = InvoiceParser()
    invoice = parser.parse_invoice(sample_invoice_texts["waves_of_harmony"])
    
    assert invoice.invoiceNumber == "WOH-2025-001"
    assert invoice.invoiceDate == "2025-03-12"
    assert invoice.dueDate == "2025-04-11"
    assert invoice.totalAmount == 290.00
    assert invoice.vendor["name"] == "Waves of Harmony Pty Ltd"
    assert invoice.participant["name"] == "Jane Doe"
    assert len(invoice.lineItems) == 2
    
    # Check line items
    assert invoice.lineItems[0].serviceDescription == "Music Therapy"
    assert invoice.lineItems[1].serviceDescription == "Equipment Rental"

def test_parse_aplus_disability_invoice(sample_invoice_texts):
    """Test parsing APLUS DISABILITY invoice."""
    parser = InvoiceParser()
    invoice = parser.parse_invoice(sample_invoice_texts["aplus_disability"])
    
    assert invoice.invoiceNumber == "APD-2025-001"
    assert invoice.invoiceDate == "2025-03-12"
    assert invoice.dueDate == "2025-04-11"
    assert invoice.totalAmount == 460.00
    assert invoice.vendor["name"] == "APLUS DISABILITY SERVICE GROUP PTY LTD"
    assert invoice.participant["name"] == "Bob Wilson"
    assert len(invoice.lineItems) == 2
    
    # Check line items
    assert invoice.lineItems[0].serviceDescription == "Support Coordination"
    assert invoice.lineItems[1].serviceDescription == "Transport Service"

def test_end_to_end_workflow(sample_invoice_texts):
    """Test complete workflow from text extraction to structured data."""
    parser = InvoiceParser()
    
    # Process multiple invoices
    invoices = []
    for vendor, text in sample_invoice_texts.items():
        invoice = parser.parse_invoice(text)
        invoices.append(invoice)
        
        # Verify common requirements
        assert invoice.invoiceNumber, f"Missing invoice number for {vendor}"
        assert invoice.invoiceDate, f"Missing invoice date for {vendor}"
        assert invoice.totalAmount > 0, f"Invalid total amount for {vendor}"
        assert invoice.vendor["name"], f"Missing vendor name for {vendor}"
        assert invoice.participant["name"], f"Missing participant name for {vendor}"
        assert invoice.lineItems, f"No line items found for {vendor}"
        
        # Verify line item calculations
        line_items_total = sum(item.lineTotal for item in invoice.lineItems)
        assert abs(line_items_total - invoice.totalAmount) < 0.01, \
            f"Line items total doesn't match invoice total for {vendor}"
        
        # Verify each line item
        for item in invoice.lineItems:
            assert item.serviceDate  # Should default to invoice date if not specified
            assert item.serviceCode  # Should be extracted or generated
            assert item.quantity > 0
            assert item.unitPrice > 0
            assert item.lineTotal > 0
            assert item.serviceDescription
            
            # Verify line item calculation
            expected_total = round(item.quantity * item.unitPrice, 2)
            assert abs(expected_total - item.lineTotal) < 0.01, \
                f"Line item calculation incorrect for {vendor}"
    
    # Verify we processed all vendors
    assert len(invoices) == 3, "Not all invoices were processed"