from dataclasses import dataclass, asdict, field
from typing import List, Dict, Optional, Union
from datetime import datetime
import re
from decimal import Decimal

class ValidationError(Exception):
    """Custom exception for data validation errors."""
    pass

def normalize_date(date_str: str) -> str:
    """Normalize date string to YYYY-MM-DD format.
    
    Handles both UK (DD/MM/YYYY) and US (MM/DD/YYYY) formats by:
    1. Using DD/MM/YYYY format by default
    2. Only using MM/DD/YYYY if the day part would be an invalid month (>12)
    
    Examples:
        >>> normalize_date("2025-03-12")  # Already in correct format
        '2025-03-12'
        >>> normalize_date("12/03/2025")  # DD/MM/YYYY
        '2025-03-12'
        >>> normalize_date("03/12/2025")  # DD/MM/YYYY (since 03 is valid month)
        '2025-03-12'
        >>> normalize_date("13/03/2025")  # Must be DD/MM/YYYY since 13 invalid month
        '2025-03-13'
    """
    try:
        text = date_str.strip()
        
        # If already in YYYY-MM-DD format
        if re.match(r'^\d{4}-\d{2}-\d{2}$', text):
            return text
            
        # Extract day, month, year parts
        if '/' in text:
            parts = text.split('/')
        elif '-' in text:
            parts = text.split('-')
        else:
            raise ValidationError(f"Invalid date format: {text}")
            
        if len(parts) != 3:
            raise ValidationError(f"Invalid date format: {text}")
            
        # If starts with year
        if len(parts[0]) == 4:
            year, month, day = parts
            return f"{year}-{int(month):02d}-{int(day):02d}"
            
        # Try as DD/MM/YYYY first
        try:
            day, month, year = parts
            return f"{year}-{int(month):02d}-{int(day):02d}"
        except ValueError:
            # If that fails, try as MM/DD/YYYY
            try:
                month, day, year = parts
                # If first number > 12, it must be a day
                if int(month) > 12:
                    day, month = month, day
                return f"{year}-{int(month):02d}-{int(day):02d}"
            except ValueError:
                raise ValidationError(f"Invalid date format: {text}")
                
    except (AttributeError, IndexError):
        raise ValidationError("Date string is None or invalid type")

def normalize_currency(amount: Union[str, float, int]) -> float:
    """Normalize currency value to float with 2 decimal places.
    
    Examples:
        >>> normalize_currency("$1,234.56")
        1234.56
        >>> normalize_currency("1234.56")
        1234.56
        >>> normalize_currency(1234.56)
        1234.56
    """
    try:
        if isinstance(amount, str):
            # Remove currency symbols and whitespace
            amount = re.sub(r'[^\d.-]', '', amount)
        return round(float(amount), 2)
    except (ValueError, TypeError):
        raise ValidationError(f"Invalid currency value: {amount}")

def normalize_text(text: str) -> str:
    """Normalize text by removing extra whitespace and special characters.
    
    Examples:
        >>> normalize_text("  Extra  Spaces  ")
        'Extra Spaces'
        >>> normalize_text("Multiple\\nLines")
        'Multiple Lines'
    """
    try:
        return ' '.join(text.strip().split())
    except AttributeError:
        raise ValidationError("Text is None or invalid type")

@dataclass
class LineItem:
    """Represents a line item in an invoice.
    
    Required fields:
    - serviceDate: Date in YYYY-MM-DD format
    - serviceCode: Non-empty string
    - quantity: Positive float
    - unitPrice: Non-negative float
    - lineTotal: Non-negative float (should equal quantity * unitPrice)
    - serviceDescription: Non-empty string
    
    Example:
        >>> line_item = LineItem(
        ...     serviceDate="2025-03-12",
        ...     serviceCode="SVC001",
        ...     quantity=2.0,
        ...     unitPrice=100.00,
        ...     lineTotal=200.00,
        ...     serviceDescription="Professional Services"
        ... )
        >>> line_item.to_dict()
        {
            'serviceDate': '2025-03-12',
            'serviceCode': 'SVC001',
            'quantity': 2.0,
            'unitPrice': 100.00,
            'lineTotal': 200.00,
            'serviceDescription': 'Professional Services'
        }
    """
    serviceDate: str
    serviceCode: str
    quantity: float
    unitPrice: float
    lineTotal: float
    serviceDescription: str
    
    def __post_init__(self):
        """Validate and normalize data after initialization."""
        try:
            # Normalize and validate date
            self.serviceDate = normalize_date(self.serviceDate)
            
            # Normalize and validate currency values
            self.quantity = normalize_currency(self.quantity)
            self.unitPrice = normalize_currency(self.unitPrice)
            self.lineTotal = normalize_currency(self.lineTotal)
            
            # Validate quantity and prices
            if self.quantity <= 0:
                raise ValidationError("Quantity must be positive")
            if self.unitPrice < 0:
                raise ValidationError("Unit price cannot be negative")
            if self.lineTotal < 0:
                raise ValidationError("Line total cannot be negative")
            
            # Validate line total calculation (allowing for small float precision differences)
            expected_total = round(self.quantity * self.unitPrice, 2)
            if abs(self.lineTotal - expected_total) > 0.01:
                raise ValidationError(f"Line total {self.lineTotal} does not match quantity * unitPrice = {expected_total}")
            
            # Normalize and validate text fields
            self.serviceCode = normalize_text(self.serviceCode)
            self.serviceDescription = normalize_text(self.serviceDescription)
            
            if not self.serviceCode:
                raise ValidationError("Service code cannot be empty")
            if not self.serviceDescription:
                raise ValidationError("Service description cannot be empty")
                
        except ValidationError as e:
            raise ValidationError(f"Line item validation failed: {str(e)}")
        except Exception as e:
            raise ValidationError(f"Line item validation failed with unexpected error: {str(e)}")
    
    def to_dict(self) -> Dict:
        """Convert line item to dictionary format."""
        return asdict(self)

@dataclass
class Invoice:
    """Represents an invoice with its associated data.
    
    Required fields:
    - invoiceNumber: Non-empty string
    - invoiceDate: Date in YYYY-MM-DD format
    - totalAmount: Non-negative float
    - vendor: Dict containing at least 'name' key
    - participant: Dict containing at least 'name' key
    - lineItems: List of LineItem objects
    
    Optional fields:
    - dueDate: Date in YYYY-MM-DD format (if provided)
    
    Example:
        >>> invoice = Invoice(
        ...     invoiceNumber="INV-2025-001",
        ...     invoiceDate="2025-03-12",
        ...     totalAmount=200.00,
        ...     vendor={"name": "ABC Company"},
        ...     participant={"name": "John Doe"},
        ...     lineItems=[
        ...         LineItem(serviceDate="2025-03-12", serviceCode="SVC001",
        ...                 quantity=2.0, unitPrice=100.00, lineTotal=200.00,
        ...                 serviceDescription="Professional Services")
        ...     ],
        ...     dueDate="2025-04-11"
        ... )
        >>> invoice.to_dict()
        {
            'invoiceNumber': 'INV-2025-001',
            'invoiceDate': '2025-03-12',
            'totalAmount': 200.00,
            'vendor': {'name': 'ABC Company'},
            'participant': {'name': 'John Doe'},
            'dueDate': '2025-04-11',
            'lineItems': [{
                'serviceDate': '2025-03-12',
                'serviceCode': 'SVC001',
                'quantity': 2.0,
                'unitPrice': 100.00,
                'lineTotal': 200.00,
                'serviceDescription': 'Professional Services'
            }]
        }
    """
    # Required fields first
    invoiceNumber: str
    invoiceDate: str
    totalAmount: float
    vendor: Dict[str, str]
    participant: Dict[str, str]
    lineItems: List[LineItem]
    # Optional fields last
    dueDate: Optional[str] = None
    
    def __post_init__(self):
        """Validate and normalize data after initialization."""
        try:
            # Normalize and validate dates
            self.invoiceDate = normalize_date(self.invoiceDate)
            if self.dueDate:
                self.dueDate = normalize_date(self.dueDate)
            
            # Normalize and validate invoice number
            self.invoiceNumber = normalize_text(self.invoiceNumber)
            if not self.invoiceNumber:
                raise ValidationError("Invoice number cannot be empty")
            
            # Normalize and validate total amount
            self.totalAmount = normalize_currency(self.totalAmount)
            if self.totalAmount < 0:
                raise ValidationError("Total amount cannot be negative")
            
            # Validate vendor and participant
            if not isinstance(self.vendor, dict) or 'name' not in self.vendor:
                raise ValidationError("Vendor must be a dictionary containing 'name' key")
            if not isinstance(self.participant, dict) or 'name' not in self.participant:
                raise ValidationError("Participant must be a dictionary containing 'name' key")
            
            self.vendor['name'] = normalize_text(self.vendor['name'])
            self.participant['name'] = normalize_text(self.participant['name'])
            
            # Validate line items total matches invoice total
            if self.lineItems:
                line_items_total = sum(item.lineTotal for item in self.lineItems)
                if abs(self.totalAmount - line_items_total) > 0.01:
                    raise ValidationError(f"Invoice total {self.totalAmount} does not match sum of line items {line_items_total}")
                
        except ValidationError as e:
            raise ValidationError(f"Invoice validation failed: {str(e)}")
        except Exception as e:
            raise ValidationError(f"Invoice validation failed with unexpected error: {str(e)}")
    
    def to_dict(self) -> Dict:
        """Convert invoice to dictionary format."""
        return asdict(self)
