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