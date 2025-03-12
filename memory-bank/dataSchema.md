# Data Schema

## Core Data Models

### Invoice
```python
@dataclass
class Invoice:
    invoiceNumber: str
    invoiceDate: str
    totalAmount: float
    vendor: Dict[str, Any]
    participant: Dict[str, Any]
    lineItems: List["LineItem"]
    dueDate: Optional[str] = None
    status: Optional[str] = None
    notes: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
```

### LineItem
```python
@dataclass
class LineItem:
    serviceDate: str
    serviceCode: str
    quantity: float
    unitPrice: float
    lineTotal: float
    serviceDescription: str
    notes: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
```

## Validation Rules

### Invoice Validation
- **invoiceNumber**: Required, non-empty string
- **invoiceDate**: Required, valid date string (YYYY-MM-DD)
- **totalAmount**: Required, positive float
- **vendor**: Required, dictionary with at least a "name" key
- **participant**: Required, dictionary with at least a "name" key
- **lineItems**: Required, non-empty list of LineItem objects
- **dueDate**: Optional, valid date string (YYYY-MM-DD) if provided
- **status**: Optional, string if provided
- **notes**: Optional, string if provided
- **metadata**: Optional, dictionary if provided

### LineItem Validation
- **serviceDate**: Required, valid date string (YYYY-MM-DD)
- **serviceCode**: Required, non-empty string
- **quantity**: Required, positive float
- **unitPrice**: Required, positive float
- **lineTotal**: Required, positive float
- **serviceDescription**: Required, non-empty string
- **notes**: Optional, string if provided
- **metadata**: Optional, dictionary if provided

## Normalization Functions

### Date Normalization
```python
def normalize_date(date_str: str) -> str:
    """
    Normalize date string to YYYY-MM-DD format.
    
    Args:
        date_str: Date string in various formats
        
    Returns:
        Normalized date string in YYYY-MM-DD format
        
    Raises:
        ValidationError: If date_str is not a valid date
    """
```

### Currency Normalization
```python
def normalize_currency(amount_str: str) -> float:
    """
    Normalize currency string to float.
    
    Args:
        amount_str: Currency string (e.g., "$1,234.56")
        
    Returns:
        Normalized float value
        
    Raises:
        ValidationError: If amount_str is not a valid currency value
    """
```

### Text Normalization
```python
def normalize_text(text: str) -> str:
    """
    Normalize text by trimming whitespace and removing control characters.
    
    Args:
        text: Input text
        
    Returns:
        Normalized text
    """
```

## Google Sheets Data Format

### Invoice Summary Format
The invoice summary format is used for the "Invoices" worksheet in Google Sheets:

| Column | Description | Source |
|--------|-------------|--------|
| Invoice Number | Unique identifier for the invoice | Invoice.invoiceNumber |
| Invoice Date | Date the invoice was issued | Invoice.invoiceDate |
| Due Date | Date the invoice is due | Invoice.dueDate |
| Vendor | Name of the vendor | Invoice.vendor["name"] |
| Participant | Name of the participant | Invoice.participant["name"] |
| Total Amount | Total amount of the invoice | Invoice.totalAmount |
| Status | Status of the invoice | Invoice.status |
| Line Items | Number of line items in the invoice | len(Invoice.lineItems) |
| Notes | Additional notes | Invoice.notes |

### Invoice Detail Format
The invoice detail format is used for the "output_invoice_data" worksheet in Google Sheets:

| Column | Description | Source |
|--------|-------------|--------|
| Invoice Number | Unique identifier for the invoice | Invoice.invoiceNumber |
| Invoice Date | Date the invoice was issued | Invoice.invoiceDate |
| Service Date | Date the service was provided | LineItem.serviceDate |
| Service Code | Code for the service | LineItem.serviceCode |
| Service Description | Description of the service | LineItem.serviceDescription |
| Quantity | Quantity of the service | LineItem.quantity |
| Unit Price | Price per unit | LineItem.unitPrice |
| Line Total | Total for the line item | LineItem.lineTotal |
| Vendor | Name of the vendor | Invoice.vendor["name"] |
| Participant | Name of the participant | Invoice.participant["name"] |
| Notes | Additional notes | LineItem.notes |

## Data Flow

1. PDF invoices are processed using OCR to extract text
2. Text is parsed using configurable regex patterns to extract structured data
3. Data is validated and normalized using the data models
4. Normalized data is converted to Google Sheets format
5. Data is stored in Google Sheets in both summary and detail formats

## Data Storage

### Google Sheets
- **Spreadsheet Name**: "NDIS-TEST"
- **Worksheets**:
  - "Invoices": Contains invoice summary data
  - "output_invoice_data": Contains invoice detail data

### Local Storage
- **PDF Invoices**: Stored in the "invoices" directory
- **OAuth Tokens**: Stored in "token.json"
- **Configuration**: Stored in "invoice_patterns.json"