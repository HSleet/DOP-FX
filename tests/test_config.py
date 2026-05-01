"""
Tests for config.py module
"""

import pytest
import json
from pathlib import Path
from config import Config


class TestConfigLoading:
    """Test configuration file loading and parsing"""

    def test_config_loads_from_file(self):
        """Test that config loads from config.json"""
        # TODO: Test actual config file loading
        config = Config("config.json")
        assert config is not None

    def test_config_file_not_found(self):
        """Test error handling when config file doesn't exist"""
        # TODO: Implement test for missing config file
        with pytest.raises(FileNotFoundError):
            Config("nonexistent_config.json")

    def test_config_invalid_json(self, tmp_path):
        """Test error handling for invalid JSON"""
        # TODO: Create invalid JSON file and test parsing
        invalid_config = tmp_path / "invalid.json"
        invalid_config.write_text("{invalid json}")
        
        with pytest.raises(json.JSONDecodeError):
            Config(str(invalid_config))


class TestConfigValues:
    """Test configuration value retrieval"""

    def test_get_database_path(self):
        """Test retrieving database path"""
        # TODO: Verify database path is correctly loaded
        config = Config("config.json")
        db_path = config.database_path
        assert isinstance(db_path, str)
        assert len(db_path) > 0

    def test_get_central_bank_url(self):
        """Test retrieving Central Bank URL"""
        # TODO: Verify URL format and validity
        config = Config("config.json")
        url = config.central_bank_url
        assert isinstance(url, str)
        assert url.startswith("https://")

    def test_get_request_timeout(self):
        """Test retrieving request timeout"""
        # TODO: Verify timeout is a reasonable number
        config = Config("config.json")
        timeout = config.request_timeout
        assert isinstance(timeout, int)
        assert timeout > 0

    def test_get_nested_value(self):
        """Test dot-separated key access"""
        # TODO: Test nested dictionary access with dot notation
        config = Config("config.json")
        value = config.get("sources.central_bank.timeout")
        assert value is not None

    def test_get_default_value(self):
        """Test default value when key doesn't exist"""
        # TODO: Verify default value is returned for missing keys
        config = Config("config.json")
        value = config.get("nonexistent.key", "default")
        assert value == "default"


class TestConfigDefaults:
    """Test configuration defaults and fallbacks"""

    def test_default_logging_level(self):
        """Test default logging level if not specified"""
        # TODO: Test fallback to default logging level
        config = Config("config.json")
        level = config.get("logging.level", "INFO")
        assert level in ["DEBUG", "INFO", "WARNING", "ERROR"]

    def test_default_database_path(self):
        """Test default database path"""
        # TODO: Test that default database path is used if not in config
        pass