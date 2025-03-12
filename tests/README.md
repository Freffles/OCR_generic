# Testing Documentation

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Install system dependencies:
- Tesseract OCR for image-based PDF processing
- Any required system libraries for PDF processing

## Test Structure

The test suite is organized into three main categories:

### 1. Unit Tests
- `test_models.py`: Tests for data models, validation, and normalization
  - Data validation functions
  - LineItem and Invoice classes
  - Error handling

### 2. Component Tests
- `test_parse_invoice.py`: Tests for invoice parsing functionality
  - Pattern configuration loading
  - Invoice type detection
  - Field extraction
  - Line item parsing

### 3. Integration Tests
- `test_integration.py`: End-to-end workflow tests
  - Multi-vendor invoice processing
  - Complete data extraction pipeline
  - Business rule validation

## Running Tests

### Run all tests:
```bash
pytest
```

### Run specific test categories:
```bash
pytest -m unit  # Run unit tests only
pytest -m integration  # Run integration tests only
```

### Run with coverage:
```bash
pytest --cov  # Generates coverage report
```

## Coverage Requirements
- Minimum coverage: 90%
- Coverage reports are generated in HTML format
- Critical components require 100% coverage:
  - Data validation
  - Error handling
  - Business rule validation

## Test Configuration

- `conftest.py`: Common test fixtures and configuration
- `pytest.ini`: Test discovery and execution settings
  - Coverage settings
  - Logging configuration
  - Test markers

## Adding New Tests

1. Follow the existing test structure
2. Add appropriate markers:
   ```python
   @pytest.mark.unit
   def test_new_feature():
       pass
   ```
3. Include test cases for:
   - Happy path
   - Edge cases
   - Error conditions
   - Business rule validation

## Test Data

- Sample invoices in various formats
- Test fixtures for different scenarios
- Mock data for external dependencies

## Continuous Integration

Tests are run automatically on:
- Pull requests
- Merges to main branch
- Release tagging

## Best Practices

1. Test one thing per test function
2. Use descriptive test names
3. Follow the Arrange-Act-Assert pattern
4. Mock external dependencies
5. Keep tests independent
6. Document test purpose and setup

## Troubleshooting

Common issues and solutions:
1. Missing dependencies: Run `pip install -r requirements.txt`
2. System library issues: Check system dependencies
3. Test discovery issues: Verify test naming conventions
4. Coverage issues: Check excluded paths in pytest.ini