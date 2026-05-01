import logging
from datetime import datetime
from typing import Optional

from config import config


def setup_logging():
    """Configure logging based on config"""
    logging.basicConfig(
        level=getattr(logging, config.get('logging.level', 'INFO')),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(config.get('logging.file', 'dop_fx.log')),
            logging.StreamHandler()
        ]
    )


def parse_date(date_str: str) -> Optional[datetime]:
    """Parse date string in various formats"""
    formats = ['%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y']
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    return None


def currency_name_from_code(code: str) -> str:
    """Get full currency name from code"""
    currency_names = {
        'USD': 'US Dollar',
        'EUR': 'Euro',
        'GBP': 'British Pound',
        'JPY': 'Japanese Yen',
        'CAD': 'Canadian Dollar',
        'CHF': 'Swiss Franc',
        'CNY': 'Chinese Yuan',
        'BRL': 'Brazilian Real',
        'AUD': 'Australian Dollar',
        'DKK': 'Danish Krone',
        'NOK': 'Norwegian Krone',
        'SEK': 'Swedish Krona',
        'SDR': 'Special Drawing Rights',
        'SSP': 'Scottish Pound'  # Note: This might be a typo in source, but keeping as is
    }
    return currency_names.get(code, code)


def validate_rate_data(data: dict) -> bool:
    """Basic validation for rate data"""
    required_fields = ['date', 'currency', 'rate']
    return all(field in data and data[field] is not None for field in required_fields)