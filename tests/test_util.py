"""
Tests for util.py module
"""

import pytest
from datetime import datetime
from util import parse_date, currency_name_from_code, validate_rate_data


class TestDateParsing:
    """Test date parsing functionality"""

    def test_parse_iso_format(self):
        """Test parsing ISO format (YYYY-MM-DD)"""
        # TODO: Implement test for ISO date format
        result = parse_date("2025-04-01")
        assert isinstance(result, datetime)
        assert result.year == 2025
        assert result.month == 4
        assert result.day == 1

    def test_parse_european_format(self):
        """Test parsing European format (DD/MM/YYYY)"""
        # TODO: Implement test for European date format
        result = parse_date("01/04/2025")
        assert isinstance(result, datetime)
        assert result.year == 2025

    def test_parse_american_format(self):
        """Test parsing American format (MM/DD/YYYY)"""
        # TODO: Implement test for American date format
        result = parse_date("04/01/2025")
        assert isinstance(result, datetime)

    def test_parse_invalid_date(self):
        """Test parsing invalid date string"""
        # TODO: Verify None is returned for invalid dates
        result = parse_date("invalid-date")
        assert result is None

    def test_parse_malformed_date(self):
        """Test parsing malformed dates"""
        # TODO: Test edge cases like invalid months/days
        result = parse_date("2025-13-45")
        assert result is None


class TestCurrencyMapping:
    """Test currency code to name mapping"""

    def test_get_currency_name_usd(self):
        """Test USD currency name lookup"""
        # TODO: Verify currency name mapping
        name = currency_name_from_code("USD")
        assert name == "US Dollar"

    def test_get_currency_name_eur(self):
        """Test EUR currency name lookup"""
        # TODO: Verify Euro currency mapping
        name = currency_name_from_code("EUR")
        assert name == "Euro"

    def test_get_currency_name_gbp(self):
        """Test GBP currency name lookup"""
        # TODO: Verify British Pound mapping
        name = currency_name_from_code("GBP")
        assert "Pound" in name

    def test_get_currency_name_unknown(self):
        """Test unknown currency code returns code itself"""
        # TODO: Verify fallback behavior for unknown codes
        name = currency_name_from_code("XYZ")
        assert name == "XYZ"

    def test_all_required_currencies(self):
        """Test that all Central Bank currencies are mapped"""
        # TODO: Add all currencies from Central Bank data
        currencies = [
            'AUD', 'BRL', 'CAD', 'CHF', 'CNY', 'SDR',
            'DKK', 'EUR', 'GBP', 'JPY', 'NOK', 'SEK'
        ]
        for currency in currencies:
            name = currency_name_from_code(currency)
            assert name is not None
            assert len(name) > 0


class TestDataValidation:
    """Test rate data validation"""

    def test_validate_complete_data(self):
        """Test validation of complete rate data"""
        # TODO: Test validation of valid data
        data = {
            'date': '2025-04-01',
            'currency': 'USD',
            'rate': 1.00
        }
        assert validate_rate_data(data) is True

    def test_validate_missing_date(self):
        """Test validation fails when date is missing"""
        # TODO: Verify validation fails for missing fields
        data = {
            'currency': 'USD',
            'rate': 1.00
        }
        assert validate_rate_data(data) is False

    def test_validate_missing_currency(self):
        """Test validation fails when currency is missing"""
        # TODO: Test missing currency field
        data = {
            'date': '2025-04-01',
            'rate': 1.00
        }
        assert validate_rate_data(data) is False

    def test_validate_missing_rate(self):
        """Test validation fails when rate is missing"""
        # TODO: Test missing rate field
        data = {
            'date': '2025-04-01',
            'currency': 'USD'
        }
        assert validate_rate_data(data) is False

    def test_validate_null_values(self):
        """Test validation fails when values are None"""
        # TODO: Test None values in required fields
        data = {
            'date': None,
            'currency': 'USD',
            'rate': 1.00
        }
        assert validate_rate_data(data) is False

    def test_validate_zero_rate(self):
        """Test validation with zero rate (edge case)"""
        # TODO: Determine if zero rates should be valid
        data = {
            'date': '2025-04-01',
            'currency': 'USD',
            'rate': 0.0
        }
        # TODO: Decide on business logic for this case
        # assert validate_rate_data(data) is False

    def test_validate_negative_rate(self):
        """Test validation with negative rate"""
        # TODO: Verify negative rates are rejected
        data = {
            'date': '2025-04-01',
            'currency': 'USD',
            'rate': -1.00
        }
        # TODO: Implement validation for negative rates
        # assert validate_rate_data(data) is False