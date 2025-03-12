# Product Context

## Project Overview
The OCR Generic project is a system for automating invoice processing using OCR (Optical Character Recognition) technology. It extracts data from PDF invoices, normalizes the data, and stores it in Google Sheets for further processing.

## Key Features
- PDF text extraction using OCR technology
- Invoice data parsing with adaptable layout recognition
- Data normalization and validation
- Google Sheets integration for data storage
- Gmail integration for email-based invoice processing
- Command-line interface for batch processing

## Technical Architecture
The system is built using Python and consists of several key components:

1. **Data Models** (models.py)
   - Defines the data structures for invoices and line items
   - Implements validation and normalization functions
   - Provides conversion utilities for different formats

2. **Invoice Parsing** (parse_invoice.py)
   - Extracts structured data from invoice text
   - Uses configurable regex patterns for adaptability
   - Handles different invoice layouts and formats
   - Implements table detection for line item extraction

3. **Text Extraction** (extract_text.py)
   - Extracts text from PDF invoices
   - Uses pdfplumber for text-based PDFs
   - Uses pytesseract for image-based PDFs
   - Determines the appropriate extraction method automatically

4. **Authentication** (oauth_handler.py, oauth_reauth.py)
   - Implements OAuth flow for Google APIs
   - Handles token storage and refresh
   - Provides error handling for authentication failures
   - Supports both Gmail and Google Sheets APIs

5. **Google Sheets Integration** (sheets_integration.py)
   - Stores invoice data in Google Sheets
   - Formats data for different sheet types
   - Implements error handling and retry logic
   - Supports batch processing for multiple invoices

6. **Gmail Integration** (planned)
   - Retrieves emails with invoice attachments
   - Extracts PDF attachments
   - Processes emails for invoice metadata
   - Handles authentication and API interactions

7. **Batch Processing** (process_invoices.py)
   - Processes multiple invoices in batch
   - Handles errors and reporting
   - Provides progress tracking
   - Implements parallel processing for efficiency

8. **Command-line Interface** (planned)
   - Provides a user-friendly interface for batch processing
   - Supports configuration options
   - Implements logging and error reporting
   - Provides help and documentation

## Data Flow
1. PDF invoices are processed using OCR to extract text
2. Text is parsed using configurable regex patterns to extract structured data
3. Data is validated and normalized using the data models
4. Normalized data is stored in Google Sheets for further processing
5. (Planned) Emails with invoice attachments are processed automatically
6. (Planned) Command-line interface provides batch processing capabilities

## Integration Points
- Google Sheets API for data storage
- Gmail API for email processing
- Local file system for PDF storage and processing

## Current Status
- Data models implemented with validation and normalization
- Invoice parsing enhanced with adaptable layout recognition
- OAuth flow adapted for single-user, dual-API access
- Google Sheets integration implemented and tested successfully
- Test infrastructure set up with unit and integration tests
- Development environment configured with requirements and linting

## Next Steps
- Enhance local PDF batch processing
- Implement Gmail integration
- Implement email information extraction
- Implement Gmail attachment OCR processing
- Implement CLI interface
- Implement comprehensive testing