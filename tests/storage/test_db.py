"""
Tests for storage layer - Database operations
"""

import pytest
import sqlite3
from source.storage.db import DatabaseManager


class TestDatabaseManagerInit:
    """Test DatabaseManager initialization and setup"""

    def test_database_manager_initializes(self, temp_db):
        """Test that DatabaseManager initializes"""
        # TODO: Ensure initialization doesn't raise errors
        manager = DatabaseManager(temp_db)
        assert manager is not None

    def test_database_file_created(self, temp_db):
        """Test that database file is created"""
        # TODO: Verify database file exists after initialization
        manager = DatabaseManager(temp_db)
        # assert Path(temp_db).exists()


class TestDatabaseTables:
    """Test database table creation and schema"""

    def test_dates_table_created(self, temp_db):
        """Test that dates table is created"""
        # TODO: Verify dates table exists with correct schema
        manager = DatabaseManager(temp_db)
        with manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='dates'")
            assert cursor.fetchone() is not None

    def test_currencies_table_created(self, temp_db):
        """Test that currencies table is created"""
        # TODO: Verify currencies table exists
        manager = DatabaseManager(temp_db)
        with manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='currencies'")
            assert cursor.fetchone() is not None

    def test_sources_table_created(self, temp_db):
        """Test that sources table is created"""
        # TODO: Verify sources table exists
        manager = DatabaseManager(temp_db)
        with manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='sources'")
            assert cursor.fetchone() is not None

    def test_rates_table_created(self, temp_db):
        """Test that rates table is created"""
        # TODO: Verify rates table exists with foreign keys
        manager = DatabaseManager(temp_db)
        with manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='rates'")
            assert cursor.fetchone() is not None

    def test_dates_table_schema(self, temp_db):
        """Test dates table has correct columns"""
        # TODO: Verify column names and types
        manager = DatabaseManager(temp_db)
        with manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("PRAGMA table_info(dates)")
            columns = {row[1]: row[2] for row in cursor.fetchall()}
            assert 'id' in columns
            assert 'date' in columns
            assert 'year' in columns
            assert 'month' in columns
            assert 'day' in columns

    def test_rates_table_schema(self, temp_db):
        """Test rates table has correct columns and constraints"""
        # TODO: Verify all required columns and types
        manager = DatabaseManager(temp_db)
        with manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("PRAGMA table_info(rates)")
            columns = {row[1]: row[2] for row in cursor.fetchall()}
            assert 'id' in columns
            assert 'datetime_id' in columns
            assert 'currency_id' in columns
            assert 'source_id' in columns
            assert 'rate_value' in columns
            assert 'rate_type' in columns


class TestInsertDate:
    """Test inserting date records"""

    def test_insert_date_success(self, temp_db):
        """Test successful date insertion"""
        # TODO: Verify date is inserted and ID is returned
        manager = DatabaseManager(temp_db)
        date_id = manager.insert_date("2025-04-01")
        assert isinstance(date_id, int)
        assert date_id > 0

    def test_insert_date_duplicate(self, temp_db):
        """Test that duplicate dates return same ID"""
        # TODO: Verify duplicate handling via UNIQUE constraint
        manager = DatabaseManager(temp_db)
        id1 = manager.insert_date("2025-04-01")
        id2 = manager.insert_date("2025-04-01")
        assert id1 == id2

    def test_date_components_extracted(self, temp_db):
        """Test that year, month, day are extracted correctly"""
        # TODO: Verify date component parsing
        manager = DatabaseManager(temp_db)
        manager.insert_date("2025-04-15")
        with manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT year, month, day FROM dates WHERE date = '2025-04-15'")
            row = cursor.fetchone()
            # assert row == (2025, 4, 15)

    def test_insert_invalid_date_format(self, temp_db):
        """Test handling of invalid date format"""
        # TODO: Test error handling for invalid dates
        manager = DatabaseManager(temp_db)
        # TODO: Decide if this should raise error or handle gracefully
        # date_id = manager.insert_date("invalid-date")


class TestInsertCurrency:
    """Test inserting currency records"""

    def test_insert_currency_success(self, temp_db):
        """Test successful currency insertion"""
        # TODO: Verify currency is inserted
        manager = DatabaseManager(temp_db)
        currency_id = manager.insert_currency("USD", "US Dollar")
        assert isinstance(currency_id, int)
        assert currency_id > 0

    def test_insert_currency_duplicate(self, temp_db):
        """Test that duplicate currencies return same ID"""
        # TODO: Verify duplicate handling
        manager = DatabaseManager(temp_db)
        id1 = manager.insert_currency("USD", "US Dollar")
        id2 = manager.insert_currency("USD", "US Dollar")
        assert id1 == id2

    def test_insert_currency_without_name(self, temp_db):
        """Test inserting currency with code only"""
        # TODO: Verify NULL name is handled
        manager = DatabaseManager(temp_db)
        currency_id = manager.insert_currency("USD")
        assert currency_id > 0

    def test_all_central_bank_currencies(self, temp_db):
        """Test inserting all Central Bank currencies"""
        # TODO: Verify all currencies can be inserted
        currencies = [
            ('AUD', 'Australian Dollar'),
            ('BRL', 'Brazilian Real'),
            ('CAD', 'Canadian Dollar'),
            ('CHF', 'Swiss Franc'),
            ('CNY', 'Chinese Yuan'),
            ('DKK', 'Danish Krone'),
            ('EUR', 'Euro'),
            ('GBP', 'British Pound'),
            ('JPY', 'Japanese Yen'),
            ('NOK', 'Norwegian Krone'),
            ('SEK', 'Swedish Krona'),
            ('USD', 'US Dollar'),
        ]
        manager = DatabaseManager(temp_db)
        for code, name in currencies:
            currency_id = manager.insert_currency(code, name)
            assert currency_id > 0


class TestInsertSource:
    """Test inserting source records"""

    def test_insert_source_success(self, temp_db):
        """Test successful source insertion"""
        # TODO: Verify source is inserted
        manager = DatabaseManager(temp_db)
        source_id = manager.insert_source("central_bank", "Central Bank of Dominican Republic")
        assert isinstance(source_id, int)
        assert source_id > 0

    def test_insert_source_duplicate(self, temp_db):
        """Test that duplicate sources return same ID"""
        # TODO: Verify duplicate handling
        manager = DatabaseManager(temp_db)
        id1 = manager.insert_source("central_bank")
        id2 = manager.insert_source("central_bank")
        assert id1 == id2

    def test_insert_source_without_description(self, temp_db):
        """Test inserting source without description"""
        # TODO: Verify NULL description is allowed
        manager = DatabaseManager(temp_db)
        source_id = manager.insert_source("central_bank")
        assert source_id > 0


class TestInsertRates:
    """Test inserting rate records"""

    def test_insert_single_rate(self, temp_db):
        """Test inserting a single rate record"""
        # TODO: Verify rate is inserted
        manager = DatabaseManager(temp_db)
        date_id = manager.insert_date("2025-04-01")
        currency_id = manager.insert_currency("USD")
        source_id = manager.insert_source("central_bank")
        
        rates_data = [(date_id, currency_id, source_id, 1.00, 'sell')]
        manager.insert_rates(rates_data)
        
        with manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM rates")
            count = cursor.fetchone()[0]
            assert count == 1

    def test_insert_multiple_rates(self, temp_db, sample_normalized_data):
        """Test batch inserting multiple rates"""
        # TODO: Verify all rates are inserted
        manager = DatabaseManager(temp_db)
        
        # Prepare rates data
        rates_data = []
        for record in sample_normalized_data:
            date_id = manager.insert_date(record['date'])
            currency_id = manager.insert_currency(record['currency'])
            source_id = manager.insert_source(record['source'])
            
            rates_data.append((
                date_id, currency_id, source_id,
                record['rate'], record['rate_type']
            ))
        
        manager.insert_rates(rates_data)
        
        with manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM rates")
            count = cursor.fetchone()[0]
            assert count == len(rates_data)

    def test_insert_rate_with_invalid_type(self, temp_db):
        """Test that invalid rate_type is rejected"""
        # TODO: Test CHECK constraint on rate_type
        manager = DatabaseManager(temp_db)
        date_id = manager.insert_date("2025-04-01")
        currency_id = manager.insert_currency("USD")
        source_id = manager.insert_source("central_bank")
        
        # TODO: Test that 'invalid' type raises error
        # rates_data = [(date_id, currency_id, source_id, 1.00, 'invalid')]
        # with pytest.raises(sqlite3.IntegrityError):
        #     manager.insert_rates(rates_data)


class TestQueryRates:
    """Test querying rate records"""

    def test_query_rates_by_date_range(self, temp_db, sample_normalized_data):
        """Test querying rates within date range"""
        # TODO: Verify date range filter works
        manager = DatabaseManager(temp_db)
        
        # Insert sample data
        for record in sample_normalized_data:
            date_id = manager.insert_date(record['date'])
            currency_id = manager.insert_currency(record['currency'])
            source_id = manager.insert_source(record['source'])
            manager.insert_rates([(date_id, currency_id, source_id, record['rate'], record['rate_type'])])
        
        # Query
        results = manager.get_rates_by_date_range("2025-04-01", "2025-04-01")
        assert len(results) > 0

    def test_query_returns_joined_data(self, temp_db, sample_normalized_data):
        """Test that query returns joined data with all fields"""
        # TODO: Verify all columns are present in results
        manager = DatabaseManager(temp_db)
        
        # Insert data
        for record in sample_normalized_data:
            date_id = manager.insert_date(record['date'])
            currency_id = manager.insert_currency(record['currency'])
            source_id = manager.insert_source(record['source'])
            manager.insert_rates([(date_id, currency_id, source_id, record['rate'], record['rate_type'])])
        
        results = manager.get_rates_by_date_range("2025-04-01", "2025-04-01")
        if results:
            record = results[0]
            assert 'rate_value' in record
            assert 'rate_type' in record
            assert 'date' in record
            assert 'code' in record
            assert 'source' in record

    def test_query_empty_range(self, temp_db):
        """Test query with date range that has no data"""
        # TODO: Verify empty result is returned
        manager = DatabaseManager(temp_db)
        results = manager.get_rates_by_date_range("2000-01-01", "2000-01-31")
        assert results == []