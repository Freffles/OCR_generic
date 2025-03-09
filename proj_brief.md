# Project Brief: Automated Invoice Extraction & Google Sheets Integration

## 1. Project Goal

To develop a Python application that automates the extraction of structured data from PDF invoices and basic email information and stores the processed information in a Google Sheet.

## 2. Key Objectives

The application will achieve the following objectives, tackled in a logical order:

1.  **Data Modeling (Foundation):** Extract key invoice details such as invoice number, invoice date, total amount, vendor information, participant information and line items. The data will be structured using Python dataclasses defined in `models.py`.
2.  **Data Normalization (Foundation):** Normalize extracted data into a consistent JSON schema to ensure data quality and consistency.
3.  **Secure Authentication (Dependency):** Use OAuth 2.0 authentication (managed by the existing `oauth_handler.py` module) for secure access to Google Sheets and Gmail.
4.  **Google Sheets Integration (Core):** Automate the process of appending normalized invoice data to the appropriate Google Sheet (`Invoices` for summary data, `output_invoice_data` for detailed data).
5.  **Local PDF Batch Processing (Mode 3 - Core):** Implement the ability to process multiple PDF invoices from a specified local folder and append the extracted data to the `output_invoice_data` sheet.
6.  **Adaptability to Invoice Layouts (Core):** Ensure the application is designed for **adaptability to different invoice layouts and formats** from various vendors. This includes employing flexible parsing techniques and configuration options to accommodate variations in invoice structures.
7.  **Gmail Integration (Mode 1/2 - Enhancement):** Integrate existing Gmail inbox processing functionality (present in `pm_main.py`) to automatically identify and categorize invoice-related emails.
8.  **Email Information Extraction (Mode 1 - Enhancement):** Extract and record basic email information (sender, subject, date, Provider, Invoice No, Amount) to the `Invoices` sheet for identified invoice emails. The `parse_email` function in `pm_parse.py` will be modified to extract these additional fields.
9.  **Gmail Attachment OCR (Mode 2 - Enhancement):** Implement Gmail attachment OCR processing to extract detailed invoice data from PDF attachments of emails identified in Gmail email processing mode. This data will be appended to the `output_invoice_data` sheet.
10. **Workflow Control & CLI Interface (Usability):** Implement a command-line interface (CLI) for mode selection. The default mode will be (1+2) (Gmail Email Processing + Attachment OCR). Users can specify `--mode 3` to run Local PDF Batch Processing exclusively.
11. **Testing (Quality Assurance):** Implement unit and integration tests to ensure the application's accuracy, reliability, and maintainability.

## 3. Modes of Operation

The application will support three primary *modes* of operation:

1.  **Gmail Email Processing (Mode 1):** Extracts summary data (Email Date, Provider, Invoice Number, Amount) from the body of identified emails and appends it to the `Invoices` sheet.
2.  **Gmail Attachment OCR Processing (Mode 2):** Extracts detailed invoice data from PDF attachments of identified emails using OCR and appends it to the `output_invoice_data` sheet.
3.  **Local PDF Batch Processing (Mode 3):** Extracts detailed invoice data from PDF files in a specified local folder using OCR and appends it to the `output_invoice_data` sheet.

## 4. Testing Strategy

The application will undergo unit tests and integration tests to ensure accuracy, reliability, and maintainability.

### 4.1 Unit Testing

**Purpose:** Validate individual components (e.g., text extraction, regex parsing, data transformation).

**Scope:**

*   Test `extract_text.py` for correct extraction from text-based PDFs.
*   Test `parse_invoice.py` for proper field extraction and JSON transformation.
*   Test `sheets_integration.py` for correctly formatting and appending invoice data to Google Sheets.
*   Mock API calls for Google Sheets and Gmail to ensure isolated function testing.

**Implementation:** Utilize `pytest` or `unittest` for structured test cases.

### 4.2 Integration Testing

**Purpose:** Validate end-to-end workflows between multiple modules.

**Scope:**

*   Ensure extracted invoice data is correctly parsed and transformed before being written to Google Sheets.
*   Verify end-to-end Gmail email processing and extraction (mocked or using a test Gmail account).
*   Simulate local PDF batch processing and confirm data consistency across all processed invoices.

**Implementation:** Use `pytest` with test cases covering full workflow execution.

## 5. Scope of Work

The project scope encompasses the following key areas:

### 5.1 Core Functionality

*   **PDF Text Extraction:** Use `pdfplumber` and `pytesseract` to extract text from PDF invoices, handling both text-based and image-based PDFs.
*   **Data Parsing & Standardization:** Implement robust data parsing and standardization techniques (including regular expressions) to extract key invoice details and transform them into a consistent JSON schema based on the `Invoice` and `LineItem` dataclasses defined in `models.py`.
*   **Google Sheets Integration:** Utilize the `gspread` library to connect to Google Sheets, authenticate using OAuth 2.0 (managed by `oauth_handler.py`), and append the extracted data to the appropriate sheet (`Invoices` or `output_invoice_data`).
*   **Local PDF Batch Processing:** Implement the ability to process multiple PDF files from a local folder.

### 5.2 Enhancement Functionality

*   **Gmail Integration:**
    *   Re-use and adapt existing code from `pm_main.py` for Gmail inbox processing, including functions for:
        *   Authenticating with the Gmail API (using `oauth_handler.py`).
        *   Searching for emails based on specified criteria (e.g., sender, subject terms).
        *   Applying labels to emails.
        *   Moving emails to a specified folder (label).
    *   Implement filtering logic based on configurable subject terms (potentially using `email_config.json`).
    *   The `fetch_gmail_labels` function in `pm_get_labels.py` can be used to retrieve available labels for the user's account.
    *   Implement functionality to download attachments from identified emails.
*   **Email Information Extraction:** Modify the `parse_email` function in `pm_parse.py` to extract Provider, Invoice Number, and Amount from the email body.
*   **Gmail Attachment OCR:** Implement OCR processing for PDF attachments.

### 5.3 Data Overview

The following data fields should be extracted from each invoice. The data will be structured according to the `Invoice` and `LineItem` dataclasses defined in `models.py`:

*   **Invoice Number:** (Required) A unique identifier for the invoice. Format: Alphanumeric (e.g., INV-2023-1234). Must match the `invoiceNumber` attribute in the `Invoice` dataclass (str).
*   **Invoice Date:** (Required) The date the invoice was issued. Format: YYYY-MM-DD. Must match the `invoiceDate` attribute in the `Invoice` dataclass (str).
*   **Total Amount:** (Required) The total amount due on the invoice, including taxes and discounts. Format: Numeric with two decimal places (e.g., 1234.56). Must match the `totalAmount` attribute in the `Invoice` dataclass (float).
*   **Vendor:** (Required) Information about the vendor. Must match the `vendor` attribute in the `Invoice` dataclass (dict). Contains at least the following:
    *   `name`: (Required) The name of the company or individual providing the goods or services (str).
*   **Participant:** (Required) Information about the recipient of the services. Must match the `participant` attribute in the `Invoice` dataclass (dict). Contains at least the following:
    *   `name`: (Required) The name of the individual or organization receiving the goods or services (str).
*   **Line Items:** (Required) A list of individual items or services included in the invoice. Must match the `lineItems` attribute in the `Invoice` dataclass (List[LineItem]). Each `LineItem` must contain the following:
    *   `serviceDate`: (Required) The date the service was provided. Format: YYYY-MM-DD. Must match the `serviceDate` attribute in the `LineItem` dataclass (str).
    *   `serviceCode`: (Required) A code identifying the service provided. Format: YYYY-MM-DD. Must match the `serviceCode` attribute in the `LineItem` dataclass (str).
    *   `quantity`: (Required) The quantity of the service provided. Must match the `quantity` attribute in the `LineItem` dataclass (float).
    *   `unitPrice`: (Required) The price per unit of the service. Must match the `unitPrice` attribute in the `LineItem` dataclass (float).
    *   `lineTotal`: (Required) The total amount for the line item (quantity * unitPrice). Must match the `lineTotal` attribute in the `LineItem` dataclass (float).
    *   `serviceDescription`: (Required) A description of the service provided. Must match the `serviceDescription` attribute in the `LineItem` dataclass (str).

### 5.4 Workflow Control & CLI Interface

The `main` function in `pm_main.py` will implement a command-line interface (CLI) to allow the user to select which processing *mode*(s) to execute.

*   **Default Mode:** Running `python pm_main.py` without arguments will execute Mode 1 + Mode 2 (Gmail Email Processing + Gmail Attachment OCR Processing) sequentially.
*   **Local PDF Batch Mode:** Passing `--mode 3` as a command-line argument (e.g., `python pm_main.py --mode 3`) will execute only Mode 3 (Local PDF Batch Processing).
*   **CLI Feedback:** The CLI will provide feedback to the user on the processing progress, including status messages and error handling information.

## 6. Deliverables

The project will deliver the following:

1.  **Python Application:** A well-structured Python application with the following modules:

    ```
    invoice_processor/
    ├── extract_text.py       # Extracts text from PDFs (reusable for local PDFs and attachments)
    ├── parse_invoice.py      # Parses extracted text into structured data
    ├── models.py             # Defines data schema using Python dataclasses
    ├── sheets_integration.py # Handles Google Sheets API connection & data upload
    ├── process_invoices.py   # Main script to run the application (handles local PDFs)
    ├── pm_main.py           # Main script for Gmail processing and workflow control & CLI
    ├── pm_parse.py           # Parses email content and extracts data
    ├── pm_get_labels.py      # Retrieves Gmail labels
    ├── oauth_handler.py      # Handles OAuth 2.0 authentication
    ├── oauth_reauth.py      # Separate script for scheduled OAuth 2.0 token refresh
    ├── requirements.txt      # List of dependencies
    ├── config.json           # Configuration file (paths, API keys, settings)
    └── email_config.json      # Configuration file (Email settings)
    ```
    (Note: The application will re-use and adapt code from existing modules like `pm_main.py`, `pm_parse.py`, and potentially `pm_get_labels.py`. The `sheets_integration.py` module will integrate with the existing OAuth flow in `oauth_handler.py`. The application will include a separate script `oauth_reauth.py` for scheduled OAuth 2.0 token refresh.)

2.  **Google Sheet:** A Google Sheet with two worksheets:
    *   `Invoices` (Summary Sheet): Stores summary data extracted from email bodies, including columns for Email Date, Provider, Invoice Number, and Amount.
    *   `output_invoice_data` (Details Sheet): Stores detailed invoice data extracted via OCR from attachments and local PDF files. This sheet will include columns corresponding to the `LineItem` dataclass, such as Service Date, Service Code, Quantity, Unit Price, Line Total, and Service Description.

3.  **README File:** A comprehensive README file with setup instructions, dependencies, usage guidelines, and configuration details. The README file will include clear instructions on how to schedule the `oauth_reauth.py` script using Windows Task Scheduler (or cron on other operating systems) to ensure regular OAuth token refresh and how to use the CLI.

4.  **Diagrams:**
    *   **Architecture Diagram:** A diagram illustrating the high-level architecture of the application, showing the main modules and their relationships, data flow, and dependencies. This diagram should clearly show the modules, data flow between modules, external dependencies (Google Sheets API, Gmail API, OCR engine), and configuration files. Consider using Mermaid syntax for creating this diagram if it enhances clarity and maintainability.
    *   **Workflow Diagram:** A diagram (e.g., flowchart or swimlane diagram) illustrating the different modes of operation (Gmail Email Processing, Gmail Attachment OCR Processing, Local PDF Batch Processing) and the steps involved in each mode. This diagram should illustrate the decision points, data transformations, and module interactions within each processing mode. Consider using Mermaid syntax for creating this diagram if it enhances clarity and maintainability.

5.  **Error Logging:** Robust error logging to track any processing failures and facilitate debugging.

## 7. Technology Stack

*   Python 3.x
*   Libraries:
    *   `pdfplumber` - Text extraction from PDFs
    *   `pytesseract` - OCR for image-based PDFs
    *   `re` - Regular expressions for data parsing
    *   `gspread` - Google Sheets integration
    *   `googleapiclient` - Gmail API interaction
    *   `oauth2client` - OAuth 2.0 handling
    *   `json` - Data formatting and configuration
    *   `os`, `glob` - File system interaction
    *   Potentially `imaplib`, `email` - Alternative Gmail interaction
    *   `oauth_reauth.py` - Separate script for scheduled OAuth 2.0 token refresh
*   Google Sheets API
*   Gmail API
*   OAuth 2.0 Authentication (managed by `oauth_handler.py`)

## 8. Success Criteria

*   The system successfully extracts invoice details (as defined in the Data Overview) with at least 95% accuracy from structured PDFs.
*   The extracted data and email information are correctly formatted and appended to the appropriate Google Sheet (`Invoices` or `output_invoice_data`).
*   The application can process multiple invoices in local batch mode (Mode 3) without errors.
*   Gmail inbox processing is successfully integrated, and invoice-related emails are correctly identified and categorized.
*   OAuth 2.0 authentication (managed by `oauth_handler.py`) securely integrates with Google Sheets and Gmail.
*   The system gracefully handles missing fields, formatting inconsistencies, and unreadable text.
*   The CLI is functional and user-friendly, allowing users to easily select and run different processing modes.
*   Unit and integration tests are implemented and pass, demonstrating the application's reliability and accuracy.

## 9. Configuration

The application will use the following configuration files:

*   `config.json`:

    ```json
    {
      "google_sheet_id": "YOUR_GOOGLE_SHEET_ID",
      "invoice_folder": "invoices/",
      "log_file": "invoice_processor.log",
      "user_folder": "rayluckins"
    }
    ```

*   `email_config.json`: Contains email settings (e.g., sender and receiver addresses) for the email notification functionality.

## 10. Next Steps

1.  Set up logging
2.  **Local PDF Batch Processing (Mode 3)** - Implement and test text extraction, data parsing, and Google Sheets integration for local PDF invoices.
3.  **Gmail Integration (Mode 1/2)** - Implement Gmail integration.
4.  **Workflow Control & CLI** - Implement the command-line interface for mode selection.
5.  **Testing** - Implement unit and integration tests.