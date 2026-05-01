"""
Shared pytest fixtures and configuration for DOP-FX tests
"""

import pytest
import sqlite3
import tempfile
import json
from pathlib import Path
from unittest.mock import Mock, patch
import sys

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture
def temp_db():
    """Create a temporary SQLite database for testing"""
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
        db_path = f.name
    
    yield db_path
    
    # Cleanup
    Path(db_path).unlink(missing_ok=True)


@pytest.fixture
def temp_config_file():
    """Create a temporary config.json for testing"""
    config_data = {
        "database": {
            "path": ":memory:"
        },
        "sources": {
            "central_bank": {
                "url": "https://www.bancentral.gov.do/a/d/2538",
                "timeout": 30
            }
        },
        "logging": {
            "level": "DEBUG",
            "file": "test.log"
        }
    }
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(config_data, f)
        config_path = f.name
    
    yield config_path
    
    # Cleanup
    Path(config_path).unlink(missing_ok=True)


@pytest.fixture
def sample_raw_data():
    """Sample raw data from Central Bank API"""
    # TODO: Create realistic sample data matching actual API response format
    return {
        "Año": 2025,
        "Mes": "04",
        "Día": "01",
        "DOLAR AUSTRALIANO": 0.65,
        "REAL BRASILENO": 0.20,
        "DOLAR CANADIENSE": 0.73,
        "FRANCO SUIZO": 1.10,
        "YUAN CHINO": 0.14,
        "DERECHO ESPECIAL DE GIRO": 1.33,
        "CORONA DANESA": 0.13,
        "EURO": 1.09,
        "LIBRA ESTERLINA": 1.27,
        "YEN JAPONES": 0.0067,
        "CORONA NORUEGA": 0.09,
        "LIBRA ESCOCESA": 1.27,  # TODO: Verify if this is correct or should be different
        "CORONA SUECA": 0.09,
        "DOLAR ESTADOUNIDENSE": 1.00
    }


@pytest.fixture
def sample_normalized_data():
    """Sample normalized rate data"""
    # TODO: Add more comprehensive test data including edge cases
    return [
        {
            'date': '2025-04-01',
            'currency': 'USD',
            'rate': 1.00,
            'source': 'central_bank',
            'rate_type': 'sell'
        },
        {
            'date': '2025-04-01',
            'currency': 'EUR',
            'rate': 1.09,
            'source': 'central_bank',
            'rate_type': 'sell'
        },
        {
            'date': '2025-04-01',
            'currency': 'GBP',
            'rate': 1.27,
            'source': 'central_bank',
            'rate_type': 'sell'
        }
    ]


@pytest.fixture
def mock_requests_get(monkeypatch):
    """Mock requests.get for API testing"""
    # TODO: Create realistic mock response matching actual API structure
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = "mocked csv data"
    mock_response.raise_for_status = Mock()
    
    def mock_get(*args, **kwargs):
        return mock_response
    
    monkeypatch.setattr("requests.get", mock_get)
    return mock_response