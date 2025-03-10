# Product Context

## Project Overview
The OCR Generic project is an automated invoice extraction and Google Sheets integration system. It aims to extract structured data from PDF invoices and store the processed information in Google Sheets, reducing manual data entry, improving efficiency, and minimizing errors.

## Key Objectives
1. Define data models for invoice details
2. Normalize extracted data into a consistent JSON schema
3. Implement secure OAuth 2.0 authentication for Google APIs
4. Integrate with Google Sheets for data storage
5. Process local PDF invoices in batch mode
6. Ensure adaptability to different invoice layouts
7. Integrate with Gmail for invoice email processing
8. Extract information from email bodies
9. Process PDF attachments from emails
10. Implement a user-friendly CLI interface
11. Ensure robust quality assurance

## Modes of Operation
1. **Gmail Email Processing (Mode 1)**: Extract summary data from email bodies
2. **Gmail Attachment OCR Processing (Mode 2)**: Extract detailed data from PDF attachments
3. **Local PDF Batch Processing (Mode 3)**: Extract detailed data from local PDF files

## Data Structure
- **Invoice**: Contains invoice number, date, due date, total amount, vendor info, participant info, and line items
- **LineItem**: Contains service date, code, quantity, unit price, line total, and description

## Technology Stack
- Python 3.x
- pdfplumber for text extraction
- pytesseract for OCR
- gspread for Google Sheets integration
- googleapiclient for Gmail API
- oauth2client for OAuth 2.0 handling

## Success Criteria
- 95% accuracy for key invoice details extraction
- Correct formatting and storage in Google Sheets
- Successful batch processing of multiple invoices
- Secure OAuth 2.0 integration
- Graceful error handling
- User-friendly CLI interface