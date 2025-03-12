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
The system uses adapters to handle different invoice formats and layouts:
- Each invoice type has its own pattern configuration
- Generic patterns serve as a fallback
- Pattern adapters normalize data to a common format

### 3. Strategy Pattern
Different strategies are used for:
- Text extraction: pdfplumber vs pytesseract
- Invoice parsing: vendor-specific vs generic patterns
- Line item extraction: table-based vs line-based

### 4. Repository Pattern
Google Sheets acts as a repository for storing processed invoice data, with clear interfaces for data access and manipulation.

### 5. Configuration Pattern
External configuration files are used to store:
- Application settings (config.json)
- Email settings (email_config.json)
- Invoice patterns (invoice_patterns.json)

## Code Patterns

### 1. Data Class Pattern
Python dataclasses are used to define structured data models for:
- Invoice data
- Line items
- Configuration settings

### 2. Factory Method Pattern
Factory methods are used to:
- Create invoice objects from raw text
- Generate appropriate parsers for different invoice types
- Create line item objects from table rows

### 3. Error Handling Pattern
Comprehensive error handling includes:
- Custom exceptions for specific error types (e.g., AuthError)
- Validation at multiple levels
- Detailed error logging with severity levels
- Graceful fallback mechanisms
- Contextual error messages with recovery suggestions

### 4. Validation Pattern
Multi-level validation is implemented:
- Data format validation
- Business rule validation
- Cross-field validation
- Total amount verification

### 5. Normalization Pattern
Data normalization is applied to:
- Dates (multiple formats to YYYY-MM-DD)
- Currency values (string to float)
- Text fields (whitespace handling)

## Integration Patterns

### 1. OAuth Authentication
OAuth 2.0 is used for secure authentication with Google APIs:
- Authorization code flow for initial authentication
- Token refresh mechanism for maintaining access
- Consolidated scopes for multiple APIs in a single flow
- Secure token storage with error handling
- Reauthorization utility for token invalidation scenarios

### 2. API Client Pattern
Wrapper classes are used to interact with external APIs (Google Sheets, Gmail), abstracting the complexity of API calls.

### 3. Batch Processing
The system processes multiple invoices in batch mode, optimizing resource usage and providing better error isolation.

## Testing Patterns

### 1. Unit Testing
Individual components are tested in isolation:
- Pattern matching functions
- Data normalization
- Validation rules
- Error handling

### 2. Integration Testing
End-to-end workflows are tested:
- PDF to structured data conversion
- Data validation and normalization
- Google Sheets integration
- Error handling and recovery

### 3. Fixture Pattern
Test fixtures are used to provide:
- Sample invoice texts
- Expected parsing results
- Mock API responses
- Error scenarios

### 4. Mock Testing Pattern
Extensive use of mocks for testing external dependencies:
- Mock file system operations
- Mock API responses
- Mock authentication flows
- Simulated error conditions

### 5. Parameterized Testing
Tests are parameterized to cover multiple scenarios:
- Different date formats
- Various invoice layouts
- Error conditions
- Edge cases