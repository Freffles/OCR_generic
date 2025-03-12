import re
import json
import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from models import Invoice, LineItem, ValidationError

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class InvoiceParsingError(Exception):
    """Custom exception for invoice parsing errors."""
    pass

class InvoiceParser:
    """Parser for extracting structured data from invoice text using configurable patterns."""
    
    def __init__(self, patterns_file: str = 'invoice_patterns.json'):
        """Initialize parser with patterns from configuration file."""
        try:
            with open(patterns_file, 'r') as f:
                self.patterns = json.load(f)['invoice_types']
            logger.info(f"Loaded patterns for {len(self.patterns)} invoice types")
        except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
            logger.error(f"Failed to load patterns file: {str(e)}")
            raise InvoiceParsingError(f"Failed to load patterns file: {str(e)}")

    def detect_invoice_type(self, text: str) -> Tuple[str, Dict]:
        """Detect invoice type based on vendor name patterns."""
        for invoice_type, config in self.patterns.items():
            if re.search(re.escape(config['name']), text, re.IGNORECASE):
                logger.info(f"Detected invoice type: {invoice_type}")
                return invoice_type, config['patterns']
        
        logger.info("No specific invoice type detected, using generic patterns")
        return 'generic', self.patterns['generic']['patterns']

    def extract_field(self, text: str, pattern: str, field_name: str) -> Optional[str]:
        """Extract field using regex pattern with error handling."""
        try:
            match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
            if match:
                return match.group(1).strip()
            logger.warning(f"Failed to extract {field_name}")
            return None
        except Exception as e:
            logger.error(f"Error extracting {field_name}: {str(e)}")
            return None

    def extract_line_items(self, text: str, patterns: Dict) -> List[LineItem]:
        """Extract line items from invoice text using table detection."""
        line_items = []
        try:
            # Find the table section
            table_text = self._extract_table_section(text, patterns['line_items'])
            if not table_text:
                logger.warning("No line items table found")
                return line_items

            # Extract rows
            rows = re.finditer(patterns['line_items']['row'], table_text, re.MULTILINE)
            for row in rows:
                try:
                    description, quantity, unit_price, total = row.groups()
                    
                    # Use today's date as service date if not found in description
                    service_date = datetime.now().strftime('%Y-%m-%d')
                    # Try to extract service date from description if present
                    date_match = re.search(r'(\d{1,2}[/\-]\d{1,2}[/\-]\d{4})', description)
                    if date_match:
                        service_date = date_match.group(1)
                    
                    # Extract service code if present, otherwise use first word of description
                    code_match = re.search(r'([A-Z0-9\-_]+):', description)
                    service_code = code_match.group(1) if code_match else description.split()[0]
                    
                    line_item = LineItem(
                        serviceDate=service_date,
                        serviceCode=service_code,
                        quantity=float(quantity),
                        unitPrice=float(unit_price.replace(',', '')),
                        lineTotal=float(total.replace(',', '')),
                        serviceDescription=description.strip()
                    )
                    line_items.append(line_item)
                except (ValueError, ValidationError) as e:
                    logger.error(f"Failed to parse line item: {str(e)}")
                    continue
                
            logger.info(f"Extracted {len(line_items)} line items")
            return line_items
        except Exception as e:
            logger.error(f"Error extracting line items: {str(e)}")
            return line_items

    def _extract_table_section(self, text: str, table_patterns: Dict) -> Optional[str]:
        """Extract the table section from invoice text."""
        try:
            start_match = re.search(table_patterns['table_start'], text, re.IGNORECASE | re.MULTILINE)
            if not start_match:
                return None
            
            end_match = re.search(table_patterns['table_end'], text[start_match.end():], re.IGNORECASE | re.MULTILINE)
            if not end_match:
                return text[start_match.end():]
            
            return text[start_match.end():start_match.end() + end_match.start()]
        except Exception as e:
            logger.error(f"Error extracting table section: {str(e)}")
            return None

    def parse_invoice(self, text: str) -> Invoice:
        """Parse invoice text into structured Invoice object."""
        try:
            # Detect invoice type and get appropriate patterns
            invoice_type, patterns = self.detect_invoice_type(text)
            
            # Extract fields using patterns
            invoice_number = self.extract_field(text, patterns['invoice_number'], 'invoice_number')
            invoice_date = self.extract_field(text, patterns['invoice_date'], 'invoice_date')
            due_date = self.extract_field(text, patterns['due_date'], 'due_date')
            total_amount = self.extract_field(text, patterns['total_amount'], 'total_amount')
            participant_name = self.extract_field(text, patterns['participant'], 'participant')
            
            if not all([invoice_number, invoice_date, total_amount]):
                raise InvoiceParsingError("Failed to extract required fields")
            
            # Extract line items
            line_items = self.extract_line_items(text, patterns)
            
            # Create Invoice object
            invoice = Invoice(
                invoiceNumber=invoice_number,
                invoiceDate=invoice_date,
                dueDate=due_date,
                totalAmount=float(total_amount.replace(',', '')),
                vendor={"name": self.patterns[invoice_type]['name']},
                participant={"name": participant_name if participant_name else "Unknown"},
                lineItems=line_items
            )
            
            logger.info(f"Successfully parsed invoice {invoice_number}")
            return invoice
            
        except ValidationError as e:
            logger.error(f"Validation error: {str(e)}")
            raise InvoiceParsingError(f"Validation error: {str(e)}")
        except Exception as e:
            logger.error(f"Failed to parse invoice: {str(e)}")
            raise InvoiceParsingError(f"Failed to parse invoice: {str(e)}")

def parse_invoice_text(raw_text: str) -> Invoice:
    """Legacy function maintained for backward compatibility."""
    parser = InvoiceParser()
    return parser.parse_invoice(raw_text)
