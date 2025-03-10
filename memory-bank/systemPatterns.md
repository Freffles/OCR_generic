# System Patterns

## Architecture Patterns

### 1. Pipeline Processing
The system uses a pipeline pattern for invoice processing:
1. Extract text from PDF
2. Parse text to identify invoice data
3. Transform data into structured format
4. Store data in Google Sheets

This pattern allows for modular development and testing of each stage independently.

### 2. Adapter Pattern
The system uses adapters to handle different invoice formats and layouts. This allows for flexibility in processing various invoice types without modifying the core processing logic.

### 3. Strategy Pattern
Different strategies are used for text extraction based on the PDF type:
- Text-based PDFs: pdfplumber strategy
- Image-based PDFs: pytesseract OCR strategy

### 4. Repository Pattern
Google Sheets acts as a repository for storing processed invoice data, with clear interfaces for data access and manipulation.

## Code Patterns

### 1. Data Class Pattern
Python dataclasses are used to define structured data models for invoices and line items, providing type hints and easy serialization.

### 2. Factory Method Pattern
Factory methods are used to create invoice objects from raw text, encapsulating the complex creation logic.

### 3. Error Handling Pattern
Try-except blocks with specific exception handling are used throughout the codebase to ensure robust error management.

### 4. Configuration Pattern
External configuration files (config.json, email_config.json) are used to store application settings, making the system more configurable without code changes.

## Integration Patterns

### 1. OAuth Authentication
OAuth 2.0 is used for secure authentication with Google APIs, following the authorization code flow pattern.

### 2. API Client Pattern
Wrapper classes are used to interact with external APIs (Google Sheets, Gmail), abstracting the complexity of API calls.

### 3. Batch Processing
The system processes multiple invoices in batch mode, optimizing resource usage and providing better error isolation.

## Testing Patterns

### 1. Unit Testing
Individual components are tested in isolation with mock dependencies.

### 2. Integration Testing
End-to-end workflows are tested to ensure components work together correctly.

### 3. Fixture Pattern
Test fixtures are used to provide consistent test data across test cases.