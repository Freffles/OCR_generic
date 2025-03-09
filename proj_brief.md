# Project Brief: Automated Invoice Extraction & Google Sheets Integration

## 1. Project Goal

To develop a Python application that automates the extraction of structured data from PDF invoices and basic email information and stores the processed information in a Google Sheet. This automation will significantly reduce manual data entry, improve efficiency in invoice processing, and minimize errors.

## 2. Key Objectives

The application will achieve the following objectives, tackled in the following logical and **dependency-driven** order:

1.  **Define Data Models (Foundation):** Design and implement Python dataclasses in `models.py` to represent key invoice details such as invoice number, invoice date, total amount, vendor information, participant information and line items. The data will be structured using Python dataclasses defined in `models.py`.
2.  **Data Normalization (Foundation):** Normalize extracted data into a consistent JSON schema to ensure data quality and consistency.
3.  **Secure Authentication (Dependency):** Use OAuth 2.0 authentication (managed by the existing `oauth_handler.py` module) for secure access to Google Sheets and Gmail.
4.  **Google Sheets Integration (Core):** Automate the process of appending normalized invoice data to the appropriate Google Sheet (`Invoices` for summary data, `output_invoice_data` for detailed data).
5.  **Local PDF Batch Processing (Mode 3 - Core):** Implement the ability to process multiple PDF invoices from a specified local folder and append the extracted data to the `output_invoice_data` sheet.
6.  **Ensure Invoice Layout Adaptability (Core & Critical):** The application **must** be designed for adaptability to different invoice layouts and formats from various vendors. This is a **core and critical requirement**, necessitating flexible parsing techniques, configuration options, and potentially machine learning approaches (if feasible within scope) to accommodate variations in invoice structures and ensure robust performance across diverse invoice types.
7.  **Gmail Integration (Mode 1/2 - Enhancement):** Integrate existing Gmail inbox processing functionality (present in `pm_main.py`) to automatically identify and categorize invoice-related emails.
8.  **Email Information Extraction (Mode 1 - Enhancement):** Extract and record basic email information (sender, subject, date, Provider, Invoice No, Amount) to the `Invoices` sheet for identified invoice emails. The `parse_email` function in `pm_parse.py` will be modified to extract these additional fields.
9.  **Gmail Attachment OCR (Mode 2 - Enhancement):** Implement Gmail attachment OCR processing to extract detailed invoice data from PDF attachments of emails identified in Gmail email processing mode. This data will be appended to the `output_invoice_data` sheet.
10. **Implement User-Friendly Workflow Control & CLI Interface (Usability):** Develop a command-line interface (CLI) to provide users with intuitive control over mode selection and application execution. The default mode will be (1+2) (Gmail Email Processing + Attachment OCR). Users can specify `--mode 3` to run Local PDF Batch Processing exclusively.
11. **Ensure Robust Quality Assurance (Testing):** Implement comprehensive unit and integration tests to ensure the application's accuracy, reliability, **and robustness**, and maintainability.

## 3. Modes of Operation

The application will support three primary *modes* of operation:

1.  **Gmail Email Processing (Mode 1):** Extracts summary data (Email Date, Provider, Invoice Number, Amount) from the body of identified emails and appends it to the `Invoices` sheet. Useful for quickly capturing key information from email notifications.
2.  **Gmail Attachment OCR Processing (Mode 2):** Extracts detailed invoice data from PDF attachments of identified emails using OCR and appends it to the `output_invoice_data` sheet. Designed for processing detailed invoice information from email attachments.
3.  **Local PDF Batch Processing (Mode 3):** Extracts detailed invoice data from PDF files in a specified local folder using OCR and appends it to the `output_invoice_data` sheet. Useful for processing invoices received outside of email or for bulk processing of historical invoices.

## 4. Testing Strategy

The application will undergo unit tests and integration tests to ensure accuracy, reliability, and maintainability.

### 4.1 Unit Testing

**Purpose:** Validate individual components (e.g., text extraction, regex parsing, data transformation).

**Scope:**

*   Test `extract_text.py` for correct extraction from text-based PDFs.
*   Test `parse_invoice.py` for proper field extraction and JSON transformation.
*   Test `sheets_integration.py` for correctly formatting and appending invoice data to Google Sheets.
*   Test `oauth_handler.py` for successful OAuth 2.0 authentication flow (mocked API calls).
*   Mock API calls for Google Sheets and Gmail to ensure isolated function testing.

**Implementation:** Utilize `pytest` or `unittest` for structured test cases.

### 4.2 Integration Testing

**Purpose:** Validate end-to-end workflows between multiple modules.

**Scope:**

*   Ensure extracted invoice data is correctly parsed and transformed before being written to Google Sheets.
*   Verify end-to-end Gmail email processing and extraction (mocked or using a test Gmail account).
*   Simulate local PDF batch processing and confirm data consistency across all processed invoices.
*   Verify robust error handling across all workflows, including cases of invalid invoice formats, missing data, and API connection failures.

**Implementation:** Use `pytest` with test cases covering full workflow execution.

## 5. Scope of Work

The project scope encompasses the following key areas:

### 5.1 Core Functionality

*   **PDF Text Extraction:** Use `pdfplumber` for text-based PDFs and `pytesseract` for image-based PDFs.  **Aim for high accuracy in OCR extraction, understanding that image quality can impact results. Document any known limitations of OCR accuracy with different invoice types.**
*   **Data Parsing & Standardization:** Implement **robust and adaptable** data parsing and standardization techniques (including regular expressions) to extract key invoice details and transform them into a consistent JSON schema based on the `Invoice` and `LineItem` dataclasses.  **This will require handling variations in invoice layouts, date formats, number formats, and vendor-specific terminology.**
*   **Google Sheets Integration:** Utilize the `gspread` library to connect to Google Sheets, authenticate using OAuth 2.0 (managed by `oauth_handler.py`), and append the extracted **summary data to the `Invoices` sheet and detailed invoice data to the `output_invoice_data` sheet.** Both `oauth_handler.py` and `oauth_reauth.py` will require modification. Existing `client_secret_<uniqueID>.json` and `token.json` are included in the root folder.
*   **Local PDF Batch Processing:** Implement the ability to process multiple PDF files from a local folder.

### 5.2 Enhancement Functionality

*   **Gmail Integration:**
    *   Re-use and **adapt and extend** existing code from `pm_main.py` for Gmail inbox processing, including functions for:
        *   Authenticating with the Gmail API (using `oauth_handler.py`).
        *   Searching for emails based on specified criteria (e.g., sender, subject terms).
        *   Applying labels to emails.
        *   Moving emails to a specified folder (label).
    *   Implement filtering logic based on configurable subject terms (potentially using `email_config.json`).
    *   The `fetch_gmail_labels` function in `pm_get_labels.py` can be used to retrieve available labels for the user's account.
    *   Implement functionality to download attachments from identified emails.
*   **Email Information Extraction:** Modify the `parse_email` function in `pm_parse.py` to extract Provider, Invoice Number, and Amount from the email body.
*   **Gmail Attachment OCR:** Implement OCR processing for PDF attachments.

### 5.2.x Code Adaptation Strategy & Guidelines

This project will leverage existing modules (`pm_main.py`, `pm_parse.py`, `pm_get_labels.py`, `oauth_handler.py`) to accelerate development and maintain consistency where possible.  However, careful adaptation is crucial to avoid code clutter and maintainability issues.  **A key area for careful adaptation is the OAuth 2.0 authentication handled by `oauth_handler.py` and `oauth_reauth.py`.** Please adhere to the following guidelines:

*   **Understand Existing Functionality, Especially OAuth:** Before adapting any module, and *especially `oauth_handler.py`*, thoroughly review its existing code and documentation (if any). **It's crucial to understand how the original multi-user, multi-app OAuth flow was implemented, even though we are simplifying it.**  Identify the parts related to user selection, app identification, and scope management.

*   **Simplify OAuth for Single-User, Dual-API (Gmail & Sheets):**  Our goal is to simplify the OAuth flow to focus on *a single user* authorizing access to *both Gmail and Google Sheets APIs* for *this specific invoice processing application*.  The provided `client_secret_<uniqueID>.json` and `token.json` in the root folder are pre-configured with the necessary scopes for both APIs, which is a great starting point.

*   **`oauth_handler.py` Adaptation - Key Areas:**  While the credentials are pre-scoped, `oauth_handler.py` likely still needs adaptation to ensure it works smoothly in our simplified context. Focus on these areas:
    *   **Remove Multi-User/Multi-App Logic:**  Identify and remove any code related to dynamically selecting users or applications.  We are now targeting a single user scenario.
    *   **Ensure Dual-API Scope Handling:** Verify that the OAuth flow in `oauth_handler.py` correctly requests and handles *both* Gmail and Google Sheets API scopes.  While the credentials are pre-scoped, the code might still have logic that expects only one scope at a time.  **Adapt it to handle both scopes within a single authentication and authorization flow.**
    *   **Static Credential Loading:**  Adapt the code to reliably load the `client_secret_<uniqueID>.json` and `token.json` from the root folder.  Ensure the paths are correctly configured and that the loading mechanism is robust.
    *   **Root Folder Credential Loading:** Ensure `oauth_handler.py` is adapted to correctly load `client_secret_<uniqueID>.json` and `token.json` specifically from the **root folder** of the `invoice_processor` directory.  The paths should be hardcoded or reliably relative to the application's root.
    *   **Focus on "One User" Authentication Flow:** Streamline the authentication process to directly authenticate *the* user associated with the provided credentials for both Gmail and Sheets.  There should be no user selection prompts or app context switching in the simplified flow.
    *   **`oauth_reauth.py` Review:**  Review `oauth_reauth.py` to ensure it remains functional in the simplified single-user, dual-API context.  It should still correctly refresh the token when needed, and the refresh process should also be scoped for both Gmail and Sheets APIs.

*   **Testing Adapted OAuth Rigorously (Crucial for Security):** **Thoroughly test the adapted OAuth flow is absolutely critical.**  Focus on these tests:
    *   **Successful Authentication & Authorization:** Verify that the application can successfully authenticate and obtain authorization for *both* Gmail and Google Sheets APIs using the provided credentials.
    *   **API Access Verification:** After successful OAuth, confirm that the application can actually *access* both the Gmail API (e.g., list emails) and the Google Sheets API (e.g., write to a sheet).
    *   **Token Refresh Functionality:** Test `oauth_reauth.py` to ensure it correctly refreshes the access token when it expires and that the refreshed token maintains access to both APIs.
    *   **Error Handling:** Test error scenarios, such as invalid credentials, missing credential files, and API access failures, and ensure graceful error handling.

*   **Modular Adaptation & Justification:** Keep OAuth-related adaptations as modular as possible within `oauth_handler.py` and `oauth_reauth.py`.  Document all changes made to these modules, clearly explaining the reasons for simplification and how the adapted code maintains security and functionality.

*   **General Code Adaptation Guidelines (Apply to all modules):**
    *   **Prioritize Extension over Modification (Where Feasible):**  Where possible, aim to extend existing functions or classes rather than directly modifying them. This can often be achieved through inheritance, composition, or adding new functions that utilize existing ones. However, for `parse_email` in `pm_parse.py`, direct modification is required as per objective 8.
    *   **Modular Adaptation:**  Try to isolate adaptations into specific functions or classes within the existing modules to make changes easier to understand and test.
    *   **Clear Justification for Modifications:**  Any direct modification of existing code (especially core modules like `oauth_handler.py`) must be clearly justified and documented. Explain *why* modification is necessary and *what potential impact* it might have on other parts of the system.
    *   **`pm_get_labels.py` Integration:** The `fetch_gmail_labels` function from `pm_get_labels.py` should be integrated into [**Specify where and how, e.g., "the initialization phase of Gmail processing (Mode 1 & 2) to dynamically retrieve available Gmail labels and allow users to configure labels in `email_config.json` using these retrieved labels instead of hardcoding them."**].  This will ensure [**Explain the benefit, e.g., "users can easily configure the application to work with their existing Gmail label structure."**]
    *   **Testing Adapted Code Rigorously:**  Adapted code must be thoroughly tested, including both unit tests for the modified parts and integration tests to ensure the adaptations work correctly within the overall application. Pay attention to potential regressions in existing functionality.
    *   **Documentation of Adaptations:**  Document all adaptations clearly, explaining the changes made, the reasons behind them, and any potential implications. Update code comments and consider adding design notes if the adaptations are complex.


### 5.3 Data Overview

The following data fields **MUST** be extracted from each invoice **wherever possible**. The data will be structured according to the `Invoice` and `LineItem` dataclasses defined in `models.py`:

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
    ├── extract_text.py       # Extracts text from PDFs (both text-based and image-based using OCR)
    ├── parse_invoice.py      # Parses extracted text to identify and structure invoice data
    ├── models.py             # Defines Python dataclasses for invoice and line item data structures
    ├── sheets_integration.py # Handles connection to Google Sheets API and data appending
    ├── process_invoices.py   # Main script for local PDF batch processing mode
    ├── pm_main.py           # Main script for Gmail processing, workflow control, and CLI
    ├── pm_parse.py           # Parses email content to extract summary invoice information
    ├── pm_get_labels.py      # Retrieves Gmail labels for email organization
    ├── oauth_handler.py      # Handles OAuth 2.0 authentication flow for Google APIs
    ├── oauth_reauth.py      # Separate script for scheduled OAuth 2.0 token refresh
    ├── requirements.txt      # List of Python dependencies
    ├── config.json           # Configuration file for application settings (paths, sheet ID, log file, etc.)
    └── email_config.json      # Configuration file for email-related settings (sender, receiver, search criteria etc.)
    ```
    (Note: The application will re-use and adapt code from existing modules like `pm_main.py`, `pm_parse.py`, and potentially `pm_get_labels.py`. The `sheets_integration.py` module will integrate with the existing OAuth flow in `oauth_handler.py`. The application will include a separate script `oauth_reauth.py` for scheduled OAuth 2.0 token refresh.)

2.  **Google Sheet:** A Google Sheet with two worksheets:
    *   `Invoices` (Summary Sheet): Stores summary data extracted from email bodies, including columns for Email Date, Provider, Invoice Number, and Amount.
    *   `output_invoice_data` (Details Sheet): Stores detailed invoice data extracted via OCR from attachments and local PDF files. This sheet will include columns corresponding to the `LineItem` dataclass, such as Service Date, Service Code, Quantity, Unit Price, Line Total, and Service Description.

3.  **README File:** A comprehensive README file **for users and future developers** with setup instructions, dependencies, usage guidelines, and configuration details. The README file will include clear instructions on how to schedule the `oauth_reauth.py` script using Windows Task Scheduler (or cron on other operating systems) to ensure regular OAuth token refresh and how to use the CLI.

4.  **Diagrams (Crucial for Understanding):**
    *   **Architecture Diagram:** A diagram illustrating the high-level architecture of the application, showing the main modules and their relationships, data flow, and dependencies. This diagram should clearly show the modules, data flow between modules, external dependencies (Google Sheets API, Gmail API, OCR engine), and configuration files. Consider using Mermaid syntax **if it enhances clarity and maintainability for the team.**
    *   **Workflow Diagram:** A diagram (e.g., flowchart or swimlane diagram) illustrating the different modes of operation (Gmail Email Processing, Gmail Attachment OCR Processing, Local PDF Batch Processing) and the steps involved in each mode. This diagram should illustrate the decision points, data transformations, and module interactions within each processing mode. Consider using Mermaid syntax **if it enhances clarity and maintainability for the team.**

5.  **Error Logging:** Robust error logging to track any processing failures and facilitate debugging.

## 7. Technology Stack

*   Python 3.x (Python 3.8+ recommended)
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
    *   `Mermaid` (if used for diagrams)
*   Google Sheets API
*   Gmail API
*   OAuth 2.0 Authentication (managed by `oauth_handler.py`)

## 8. Success Criteria

*   The system successfully extracts **key** invoice details (Invoice Number, Invoice Date, Total Amount, Vendor Name, Participant Name) with at least 95% accuracy from structured PDFs. **Line item extraction accuracy may be lower initially and will be iteratively improved.**
*   The extracted data and email information are correctly formatted and appended to the appropriate Google Sheet (`Invoices` or `output_invoice_data`).
*   The application can process multiple invoices in local batch mode (Mode 3) without errors.
*   Gmail inbox processing is successfully integrated, and invoice-related emails are correctly identified and categorized.
*   OAuth 2.0 authentication (managed by `oauth_handler.py`) securely integrates with Google Sheets and Gmail.
*   The system gracefully handles missing fields, formatting inconsistencies, and unreadable text.
*   The CLI is functional and user-friendly, allowing users to easily select and run different processing modes.
*   Unit and integration tests are implemented and **all critical tests** pass, demonstrating the application's reliability and accuracy.
*   The system **gracefully handles errors and provides informative logging** for debugging and issue resolution.

## 9. Configuration

The application will use the following configuration files:

*   `config.json`:

    ```json
    {
      "google_sheet_id": "YOUR_GOOGLE_SHEET_ID",
      "invoice_folder": "invoices/",
      "log_file": "invoice_processor.log"
    }
    ```
    This file contains application-level configuration settings.
    *   `google_sheet_id`:  **(Required)**  The ID of the Google Sheet where invoice data will be stored. You can find this ID in the URL of your Google Sheet.
    *   `invoice_folder`:  **(Required for Mode 3)** The path to the local folder where PDF invoices are stored for batch processing.
    *   `log_file`:  **(Optional)** The path and filename for the application's log file.

*   `email_config.json`: Contains email settings (e.g., sender and receiver addresses, email search criteria) for the Gmail processing functionality.

**Important: OAuth 2.0 Credentials**

For secure access to Google Sheets and Gmail APIs, the application relies on OAuth 2.0. The following credential files are **required** and must be placed in the **root folder**:

*   `client_secret_<uniqueID>.json`:  **(Required)** Contains your Google API client secrets. You should have already downloaded this file from the Google Cloud Console when setting up your API project and OAuth 2.0 credentials. **Ensure this `client_secret_<uniqueID>.json` is configured with scopes for both Google Sheets API and Gmail API.**
*   `token.json`:  This file will be automatically generated after the first successful OAuth 2.0 authorization flow. It stores the user's access and refresh tokens. **Do not manually create this file.** The `oauth_handler.py` module will handle its creation and refresh.

Existing credentials in client_secret_<uniqueID>.json and token.json are correctly scoped for Gmail and Google Sheets. These files should be used as-is without renaming, as Google OAuth requires the original filename format.

In previous iterations of related projects, a `user_folder` configuration might have been used for managing user-specific settings in a multi-user environment.  However, **for this simplified invoice processing application, which focuses on a single user and dual-API access, the `user_folder` configuration is no longer relevant and has been removed from `config.json` for clarity.**  All necessary configuration for this application is now contained in `config.json`, `email_config.json`, and the root-level credential files (`client_secret_<uniqueID>.json` and `token.json`).

## 10. Next Steps

1.  Set up logging
2.  **Local PDF Batch Processing (Mode 3)** - Implement and test text extraction, data parsing, and Google Sheets integration for local PDF invoices.
3.  **Gmail Integration (Mode 1/2)** - Implement Gmail integration.
4.  **Workflow Control & CLI** - Implement the command-line interface for mode selection.
5.  **Testing** - Implement unit and integration tests.