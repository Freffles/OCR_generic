# Decision Log

## Decision 001: PDF Text Extraction Approach
- **Date**: 2025-03-10
- **Context**: Need to extract text from PDF invoices, which may be text-based or image-based.
- **Options Considered**:
  1. Use pdfplumber for all PDFs
  2. Use pytesseract for all PDFs
  3. Use pdfplumber for text-based PDFs and pytesseract for image-based PDFs
- **Decision**: Option 3 - Use pdfplumber for text-based PDFs and pytesseract for image-based PDFs
- **Rationale**: pdfplumber is more efficient and accurate for text-based PDFs, while pytesseract is necessary for image-based PDFs. This hybrid approach optimizes both performance and accuracy.
- **Consequences**: Need to implement logic to determine if a PDF is text-based or image-based.

## Decision 002: Data Structure Approach
- **Date**: 2025-03-10
- **Context**: Need to define a consistent data structure for invoice information.
- **Options Considered**:
  1. Use dictionaries
  2. Use custom classes
  3. Use dataclasses
- **Decision**: Option 3 - Use dataclasses
- **Rationale**: Dataclasses provide type hints, are more maintainable, and can be easily converted to dictionaries or JSON.
- **Consequences**: Need to ensure all extracted data conforms to the dataclass structure.

## Decision 003: OAuth Authentication Approach
- **Date**: 2025-03-10
- **Context**: Need to authenticate with Google APIs (Sheets and Gmail).
- **Options Considered**:
  1. Keep multi-user, multi-app OAuth flow
  2. Simplify to single-user, dual-API OAuth flow
- **Decision**: Option 2 - Simplify to single-user, dual-API OAuth flow
- **Rationale**: The project only needs to authenticate a single user for both Gmail and Google Sheets APIs, so a simplified approach is more appropriate.
- **Consequences**: Need to adapt existing oauth_handler.py and oauth_reauth.py to handle both APIs in a single flow.

## Decision 004: Invoice Parsing Approach
- **Date**: 2025-03-10
- **Context**: Need to extract structured data from invoice text.
- **Options Considered**:
  1. Use fixed regex patterns
  2. Use configurable regex patterns
  3. Use machine learning
- **Decision**: Option 2 - Use configurable regex patterns
- **Rationale**: Configurable regex patterns provide flexibility to handle different invoice formats while being simpler to implement than machine learning.
- **Consequences**: Need to develop a configuration system for regex patterns.

## Decision 005: Invoice Pattern Configuration Approach
- **Date**: 2025-03-12
- **Context**: Need to implement adaptable invoice parsing for different layouts.
- **Options Considered**:
  1. Hardcode patterns in code
  2. Use JSON configuration file
  3. Use database storage
- **Decision**: Option 2 - Use JSON configuration file
- **Rationale**: JSON configuration provides flexibility to add/modify patterns without code changes, while being simpler than database storage.
- **Consequences**: Need to maintain and validate pattern configurations.

## Decision 006: Line Item Extraction Strategy
- **Date**: 2025-03-12
- **Context**: Need to extract line items from invoice tables.
- **Options Considered**:
  1. Simple line-by-line parsing
  2. Table structure detection
  3. Machine learning-based table extraction
- **Decision**: Option 2 - Table structure detection
- **Rationale**: Table structure detection provides better accuracy than line-by-line parsing while being more practical than ML approach.
- **Consequences**: Need to handle variations in table formats and layouts.

## Decision 007: OAuth Implementation Details
- **Date**: 2025-03-12
- **Context**: Need to implement the simplified OAuth flow for single-user, dual-API access.
- **Options Considered**:
  1. Modify existing code with minimal changes
  2. Complete rewrite with new architecture
  3. Hybrid approach with significant refactoring
- **Decision**: Option 3 - Hybrid approach with significant refactoring
- **Rationale**: The existing code had multi-user logic deeply embedded, requiring significant changes. A complete rewrite would lose valuable error handling and token management logic. The hybrid approach preserves the best parts while simplifying the overall architecture.
- **Consequences**:
  - Simplified API with clearer function names and parameters
  - Improved error handling with custom AuthError class
  - Better logging for debugging authentication issues
  - Consolidated token storage for both API scopes
  - Need for comprehensive testing to ensure reliability

## Decision 008: Google Sheets Integration Approach
- **Date**: 2025-03-12
- **Context**: Need to implement Google Sheets integration for storing invoice data.
- **Options Considered**:
  1. Use service account authentication
  2. Use OAuth user authentication
  3. Support both authentication methods
- **Decision**: Option 2 - Use OAuth user authentication
- **Rationale**: OAuth user authentication aligns with the single-user approach already implemented for Gmail integration, allowing both APIs to use the same authentication flow and token.
- **Consequences**:
  - Need to update existing sheets_integration.py to use the OAuth flow
  - Simplified authentication management with a single flow for both APIs
  - User will need to grant permissions for both APIs in one flow

## Decision 009: Google Sheets Data Storage Format
- **Date**: 2025-03-12
- **Context**: Need to define how invoice data will be stored in Google Sheets.
- **Options Considered**:
  1. Store all data in a single sheet with complex structure
  2. Use multiple sheets with different levels of detail
  3. Use a single sheet with flattened data structure
- **Decision**: Option 2 - Use multiple sheets with different levels of detail
- **Rationale**: This approach provides both summary views (Invoices sheet) and detailed views (output_invoice_data sheet), making the data more accessible and usable for different purposes.
- **Consequences**:
  - Need to implement different formatting functions for each sheet type
  - Need to ensure data consistency between sheets
  - More flexible reporting capabilities

## Decision 010: Error Handling and Retry Strategy
- **Date**: 2025-03-12
- **Context**: Need to handle API errors and transient failures when interacting with Google Sheets.
- **Options Considered**:
  1. Simple error reporting without retries
  2. Retry with exponential backoff
  3. Retry with fixed delay
- **Decision**: Option 3 - Retry with fixed delay
- **Rationale**: Fixed delay retries are simpler to implement and sufficient for most transient API errors, while still providing resilience against temporary failures.
- **Consequences**:
  - More robust API interactions
  - Need to implement retry logic for all API calls
  - Need to handle permanent failures gracefully

## Decision 011: Google Drive API Scope Requirement
- **Date**: 2025-03-12
- **Context**: Google Sheets integration requires access to the Drive API to list and access spreadsheets.
- **Options Considered**:
  1. Use only the Sheets API scope
  2. Use both Sheets API and Drive API scopes
  3. Use a custom limited scope
- **Decision**: Option 2 - Use both Sheets API and Drive API scopes
- **Rationale**: The Google Sheets API requires Drive API access to list and find spreadsheets by name. Without the Drive API scope, the application cannot access spreadsheets by name, only by ID.
- **Consequences**:
  - Need to update OAuth scopes to include Drive API
  - User needs to grant additional permissions
  - More comprehensive access to Google Drive resources
  - Successfully tested with real Google Sheets