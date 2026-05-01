# DOP-FX Test Suite

Comprehensive test suite for the DOP-FX foreign exchange rate tracking system.

## Test Structure

```
tests/
├── conftest.py                           # Shared pytest fixtures and configuration
├── test_config.py                        # Configuration module tests
├── test_util.py                          # Utility functions tests
├── ingestion/
│   └── test_central_bank_ingestor.py    # Data fetching/ingestion tests
├── normalization/
│   └── test_central_bank_normalizer.py  # Data transformation tests
├── storage/
│   ├── test_db.py                       # Database layer tests
│   └── test_storage_manager.py          # High-level storage operations tests
└── integration/
    └── test_pipeline.py                 # End-to-end pipeline tests
```

## Test Categories

### Unit Tests

**test_config.py** - Configuration Loading and Management
- Config file loading and parsing
- Configuration value retrieval
- Default values and fallbacks
- Error handling for missing/invalid config

**test_util.py** - Utility Functions
- Date parsing (multiple formats)
- Currency code to name mapping
- Data validation functions
- Error handling

**test_central_bank_ingestor.py** - Data Ingestion
- API connectivity and data fetching
- Response parsing and formatting
- Error handling (timeouts, connection errors, HTTP errors)
- Daily vs historical data handling

**test_central_bank_normalizer.py** - Data Normalization
- Raw data transformation
- Schema mapping (column names to field names)
- Date component extraction
- Currency code mapping
- Data validation during normalization

**test_db.py** - Database Operations
- Table creation and schema verification
- CRUD operations (Create, Read)
- Foreign key relationships
- Data integrity constraints
- Query functionality

**test_storage_manager.py** - Storage Operations
- Storing normalized data
- Reference creation (dates, currencies, sources)
- Duplicate handling
- Error handling and logging

### Integration Tests

**test_pipeline.py** - Full Pipeline
- End-to-end pipeline execution (ingest → normalize → store)
- Component integration
- Data consistency across stages
- Error recovery
- Performance with large datasets
- Idempotency (duplicate runs produce same result)
- Multi-source handling

## Running Tests

### Run all tests
```bash
pytest
```

### Run with coverage
```bash
pytest --cov=source
```

### Run specific test file
```bash
pytest tests/test_config.py
```

### Run specific test class
```bash
pytest tests/test_config.py::TestConfigLoading
```

### Run specific test
```bash
pytest tests/test_config.py::TestConfigLoading::test_config_loads_from_file
```

### Run only unit tests
```bash
pytest -m unit
```

### Run tests with verbose output
```bash
pytest -v
```

### Run tests in parallel (requires pytest-xdist)
```bash
pytest -n auto
```

## Fixtures

Common pytest fixtures defined in `conftest.py`:

- **temp_db** - Temporary SQLite database for testing
- **temp_config_file** - Temporary configuration file
- **sample_raw_data** - Sample raw data from Central Bank
- **sample_normalized_data** - Sample normalized rate data
- **mock_requests_get** - Mocked requests.get for API testing

## Test Coverage

Target coverage areas:
- Core functionality: ≥85%
- Error paths: ≥80%
- Integration workflows: ≥75%

## TODO Markers

Throughout the test suite, `# TODO:` markers indicate:
- Tests that need implementation details
- Missing mock data or fixtures
- Validation logic that needs to be defined
- Performance requirements to be established
- Edge cases to consider

These should be addressed as implementation progresses.

## Common Patterns

### Testing with fixtures
```python
def test_something(temp_db, sample_normalized_data):
    manager = DatabaseManager(temp_db)
    # test code here
```

### Mocking external calls
```python
def test_api_call(mock_requests_get):
    ingestor = CentralBankIngestor()
    result = ingestor.fetch_data()
    # assertions here
```

### Testing database operations
```python
def test_db_operation(temp_db):
    manager = DatabaseManager(temp_db)
    with manager.get_connection() as conn:
        cursor = conn.cursor()
        # test queries here
```

## Dependencies

Required for testing:
- pytest>=7.0.0
- pytest-cov>=3.0.0
- pytest-mock (for additional mocking features)

Install with:
```bash
pip install -e ".[dev]"
```
