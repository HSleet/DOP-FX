from typing import List, Dict, Any
import logging

from .db import db_manager
from util import setup_logging

logger = logging.getLogger(__name__)


class StorageManager:
    def __init__(self):
        setup_logging()

    def store_normalized_data(self, normalized_data: List[Dict[str, Any]]):
        """Store normalized rate data in database"""
        if not normalized_data:
            logger.warning("No data to store")
            return

        try:
            # Prepare data for batch insert
            rates_to_insert = []

            for record in normalized_data:
                # Get or create IDs
                date_id = db_manager.insert_date(record['date'])
                currency_id = db_manager.insert_currency(
                    record['currency'],
                    currency_name_from_code(record['currency'])
                )
                source_id = db_manager.insert_source(
                    record['source'],
                    f"{record['source'].replace('_', ' ').title()} Data Source"
                )

                rates_to_insert.append((
                    date_id,
                    currency_id,
                    source_id,
                    record['rate'],
                    record.get('rate_type', 'sell')
                ))

            # Batch insert rates
            db_manager.insert_rates(rates_to_insert)
            logger.info(f"Stored {len(rates_to_insert)} rate records")

        except Exception as e:
            logger.error(f"Failed to store data: {e}")
            raise

    def query_rates(self, start_date: str, end_date: str) -> List[Dict]:
        """Query stored rates"""
        return db_manager.get_rates_by_date_range(start_date, end_date)