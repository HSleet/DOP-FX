import pandas as pd
from typing import List, Dict, Any
import logging

from util import currency_name_from_code, validate_rate_data, setup_logging

logger = logging.getLogger(__name__)


class CentralBankNormalizer:
    def __init__(self):
        setup_logging()

    def normalize_historical_data(self, raw_data: pd.DataFrame) -> List[Dict[str, Any]]:
        """Normalize historical data from Central Bank format"""
        normalized_data = []

        if raw_data.empty:
            logger.warning("Empty raw data provided")
            return normalized_data

        # Currency code mapping from column names
        currency_mapping = {
            'DOLAR AUSTRALIANO': 'AUD',
            'REAL BRASILENO': 'BRL',
            'DOLAR CANADIENSE': 'CAD',
            'FRANCO SUIZO': 'CHF',
            'YUAN CHINO': 'CNY',
            'DERECHO ESPECIAL DE GIRO': 'SDR',
            'CORONA DANESA': 'DKK',
            'EURO': 'EUR',
            'LIBRA ESTERLINA': 'GBP',
            'YEN JAPONES': 'JPY',
            'CORONA NORUEGA': 'NOK',
            'LIBRA ESCOCESA': 'SSP',  # Assuming this is Scottish Pound
            'CORONA SUECA': 'SEK',
            'DOLAR ESTADOUNIDENSE': 'USD'
        }

        for _, row in raw_data.iterrows():
            year = row['Año']
            month = row['Mes']
            day = row['Día']

            # Create date string
            date_str = "04d"

            for currency_col, currency_code in currency_mapping.items():
                if currency_col in row and pd.notna(row[currency_col]):
                    rate_data = {
                        'date': date_str,
                        'currency': currency_code,
                        'rate': float(row[currency_col]),
                        'source': 'central_bank',
                        'rate_type': 'sell'  # Assuming sell rates from Central Bank
                    }

                    if validate_rate_data(rate_data):
                        normalized_data.append(rate_data)
                    else:
                        logger.warning(f"Invalid rate data: {rate_data}")

        logger.info(f"Normalized {len(normalized_data)} rate records")
        return normalized_data

    def normalize_daily_data(self, daily_data: dict) -> List[Dict[str, Any]]:
        """Normalize daily rate data"""
        # TODO: Implement daily data normalization
        logger.info("Normalizing daily data...")
        return []