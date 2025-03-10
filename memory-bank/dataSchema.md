# Invoice Data Schema

## Overview
This document defines the unified schema for invoice data extraction. This schema represents the data structure that should be extracted from invoices whenever available.

## JSON Schema

```json
{
  "invoice": {
    "invoiceNumber": "",
    "invoiceDate": "",
    "dueDate": "",
    "totalAmount": 0,
    "vendor": {
      "name": ""
    },
    "participant": {
      "name": ""
    },
    "lineItems": [
      {
        "serviceDate": "",
        "serviceCode": "",
        "quantity": 0,
        "unitPrice": 0,
        "lineTotal": 0,
        "serviceDescription": ""
      }
      // Additional line items can be added here
    ]
  }
}
```

## Field Descriptions

### Invoice Fields
- **invoiceNumber**: A unique identifier for the invoice (string)
- **invoiceDate**: The date the invoice was issued in YYYY-MM-DD format (string)
- **dueDate**: The date payment is due in YYYY-MM-DD format (string)
- **totalAmount**: The total amount due on the invoice (number)
- **vendor**: Information about the vendor (object)
  - **name**: The name of the company or individual providing the goods or services (string)
- **participant**: Information about the recipient of the services (object)
  - **name**: The name of the individual or organization receiving the goods or services (string)
- **lineItems**: A list of individual items or services included in the invoice (array of objects)

### Line Item Fields
- **serviceDate**: The date the service was provided in YYYY-MM-DD format (string)
- **serviceCode**: A code identifying the service provided (string)
- **quantity**: The quantity of the service provided (number)
- **unitPrice**: The price per unit of the service (number)
- **lineTotal**: The total amount for the line item (quantity * unitPrice) (number)
- **serviceDescription**: A description of the service provided (string)

## Data Extraction Priority
When extracting data from invoices, the system should prioritize fields in the following order:
1. Required fields: invoiceNumber, invoiceDate, totalAmount, vendor.name, participant.name
2. Important fields: dueDate, lineItems (if available)
3. Detailed fields: individual line item details

## Handling Missing Data
- If a required field is missing, the system should log a warning and continue processing
- If a field is not found in the invoice, it should be left empty (for strings) or set to 0 (for numbers)
- The system should never fail completely due to missing fields, but should provide clear logging about what data could not be extracted

## Data Normalization Rules
- Dates should be normalized to YYYY-MM-DD format
- Currency values should be normalized to numbers without currency symbols
- Text fields should have leading/trailing whitespace removed
- Line items should be extracted as completely as possible, but partial line items are acceptable if some fields cannot be extracted