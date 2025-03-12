# System Patterns

## Design Patterns

### 1. Factory Pattern
- **Used In**: extract_text.py
- **Purpose**: Creates appropriate text extractor based on PDF type
- **Implementation**: Factory function that determines if a PDF is text-based or image-based and returns the appropriate extractor

### 2. Strategy Pattern
- **Used In**: parse_invoice.py
- **Purpose**: Allows different parsing strategies based on invoice type
- **Implementation**: Configurable regex patterns in invoice_patterns.json

### 3. Adapter Pattern
- **Used In**: sheets_integration.py
- **Purpose**: Adapts Invoice objects to Google Sheets row format
- **Implementation**: Functions that convert Invoice objects to row arrays for Google Sheets

### 4. Decorator Pattern
- **Used In**: oauth_handler.py
- **Purpose**: Adds authentication and retry functionality to API calls
- **Implementation**: Wrapper functions that handle authentication and retries

### 5. Repository Pattern
- **Used In**: sheets_integration.py
- **Purpose**: Abstracts data storage operations
- **Implementation**: Functions that handle CRUD operations on Google Sheets

### 6. Retry Pattern
- **Used In**: sheets_integration.py
- **Purpose**: Handles transient API failures
- **Implementation**: Retry logic with fixed delay for API calls

## Architectural Patterns

### 1. Layered Architecture
- **Layers**:
  - Data Access Layer (extract_text.py, sheets_integration.py)
  - Business Logic Layer (parse_invoice.py, models.py)
  - Presentation Layer (process_invoices.py, CLI interface)
- **Purpose**: Separation of concerns, maintainability

### 2. Service-Oriented Architecture
- **Services**:
  - Text Extraction Service (extract_text.py)
  - Invoice Parsing Service (parse_invoice.py)
  - Data Storage Service (sheets_integration.py)
  - Authentication Service (oauth_handler.py)
- **Purpose**: Modularity, reusability

## Code Patterns

### 1. Error Handling
- **Pattern**: Try-except blocks with specific exception types
- **Purpose**: Robust error handling
- **Example**:
  ```python
  try:
      # Operation that might fail
  except SpecificError as e:
      # Handle specific error
  except Exception as e:
      # Handle general error
  ```

### 2. Logging
- **Pattern**: Hierarchical logging with different levels
- **Purpose**: Debugging, monitoring
- **Example**:
  ```python
  logger = logging.getLogger(__name__)
  logger.info("Informational message")
  logger.warning("Warning message")
  logger.error("Error message")
  ```

### 3. Configuration
- **Pattern**: External configuration files
- **Purpose**: Flexibility, maintainability
- **Example**: invoice_patterns.json for configurable regex patterns

### 4. Validation
- **Pattern**: Input validation with clear error messages
- **Purpose**: Data integrity, user feedback
- **Example**: Validation functions in models.py

### 5. Normalization
- **Pattern**: Data normalization functions
- **Purpose**: Consistent data format
- **Example**: Date and currency normalization in models.py

### 6. Batch Processing
- **Pattern**: Process multiple items in batch
- **Purpose**: Efficiency, performance
- **Example**: Batch processing in sheets_integration.py and process_invoices.py

### 7. Retry Logic
- **Pattern**: Retry operations with delay
- **Purpose**: Resilience against transient failures
- **Example**: API calls in sheets_integration.py

### 8. Authentication
- **Pattern**: OAuth flow with token refresh
- **Purpose**: Secure API access
- **Example**: OAuth implementation in oauth_handler.py

### 9. Data Formatting
- **Pattern**: Multiple data representations for different purposes
- **Purpose**: Flexibility, usability
- **Example**: Summary and detailed formats in sheets_integration.py