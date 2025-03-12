# Testing Strategy

## Testing Approach

The OCR Generic project follows a comprehensive testing approach that includes:

1. **Unit Testing**: Testing individual components in isolation
2. **Component Testing**: Testing interactions between related components
3. **Integration Testing**: Testing end-to-end workflows
4. **Mock Testing**: Using mocks to simulate external dependencies
5. **Real-World Testing**: Testing with actual external services

## Test Types

### Unit Tests
- **Purpose**: Verify that individual functions and methods work correctly in isolation
- **Tools**: pytest, unittest.mock
- **Coverage Target**: 80% code coverage
- **Examples**:
  - Testing validation functions in models.py
  - Testing regex pattern matching in parse_invoice.py
  - Testing authentication functions in oauth_handler.py

### Component Tests
- **Purpose**: Verify that related components work correctly together
- **Tools**: pytest, unittest.mock
- **Coverage Target**: 70% code coverage
- **Examples**:
  - Testing invoice parsing with different invoice types
  - Testing OAuth flow with token refresh
  - Testing Google Sheets formatting functions

### Integration Tests
- **Purpose**: Verify that end-to-end workflows work correctly
- **Tools**: pytest, unittest.mock
- **Coverage Target**: 60% code coverage
- **Examples**:
  - Testing PDF extraction to Google Sheets workflow
  - Testing email processing workflow
  - Testing batch processing workflow

### Mock Tests
- **Purpose**: Test interactions with external services without actually calling them
- **Tools**: unittest.mock, pytest-mock
- **Coverage Target**: 90% of external service interactions
- **Examples**:
  - Mocking Google Sheets API calls
  - Mocking Gmail API calls
  - Mocking OAuth authentication

### Real-World Tests
- **Purpose**: Verify that the system works correctly with actual external services
- **Tools**: pytest, actual Google APIs
- **Coverage Target**: Key workflows and edge cases
- **Examples**:
  - Testing with actual Google Sheets (test_sheets_real.py)
  - Testing with actual Gmail
  - Testing with actual PDF invoices

## Test Implementation

### Test Directory Structure
```
tests/
  ├── conftest.py           # Shared fixtures and utilities
  ├── test_models.py        # Unit tests for data models
  ├── test_parse_invoice.py # Unit tests for invoice parsing
  ├── test_oauth.py         # Unit tests for OAuth flow
  ├── test_sheets_integration.py # Unit tests for Google Sheets integration
  ├── test_integration.py   # Integration tests for workflows
  └── README.md             # Test documentation
```

### Test Fixtures
- **PDF Fixtures**: Sample PDF invoices for testing
- **Mock Fixtures**: Mock objects for external services
- **Data Fixtures**: Sample data for testing

### Test Coverage
- **Tool**: pytest-cov
- **Command**: `pytest --cov=. tests/`
- **Current Coverage**:
  - models.py: 92%
  - parse_invoice.py: 85%
  - oauth_handler.py: 87%
  - oauth_reauth.py: 76%
  - sheets_integration.py: 67%
  - Overall: 81%

## Testing Guidelines

### Writing Tests
1. Each test should have a clear purpose and description
2. Tests should be independent and not rely on other tests
3. Tests should be deterministic and not depend on external state
4. Tests should be fast and efficient
5. Tests should cover both happy paths and error cases

### Test Naming
- Test names should be descriptive and follow the pattern `test_<function_name>_<scenario>`
- Example: `test_parse_invoice_valid_input`, `test_parse_invoice_missing_field`

### Test Documentation
- Each test file should have a docstring explaining its purpose
- Complex tests should have comments explaining their logic
- Test fixtures should be documented in conftest.py

## Continuous Integration

### CI Pipeline
- **Tool**: GitHub Actions
- **Triggers**: Push to main branch, pull requests
- **Steps**:
  1. Install dependencies
  2. Run linting
  3. Run tests
  4. Generate coverage report
  5. Deploy (if on main branch)

### Test Automation
- **Schedule**: Daily automated tests
- **Scope**: All tests, including real-world tests
- **Reporting**: Email notification on failure

## Recent Testing Achievements

- Implemented comprehensive unit tests for models.py with 92% coverage
- Added component tests for parse_invoice.py with 85% coverage
- Created mock tests for oauth_handler.py with 87% coverage
- Implemented mock tests for sheets_integration.py with 67% coverage
- Created real-world test script (test_sheets_real.py) for testing with actual Google Sheets
- Successfully tested Google Sheets integration with real data