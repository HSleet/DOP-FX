import requests
from datetime import datetime
import logging
from io import BytesIO
import polars as pl
from typing import Optional

# from config import config
# from util import setup_logging

logger = logging.getLogger(__name__)

# hardcode config and logging for testing
class config:
    central_bank_url = "https://cdn.bancentral.gov.do/documents/estadisticas/mercado-cambiario/documents/TASAS_CONVERTIBLES_OTRAS_MONEDAS.xlsx"
    request_timeout = 10
def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler("logs/ingestion.log"),
            logging.StreamHandler()
        ]
    )

class CentralBankIngestor:
    def __init__(self):
        setup_logging()

    def fetch_data(self) -> Optional[pl.DataFrame]:
        """Fetch FX data from Central Bank"""
        url = config.central_bank_url
        timeout = config.request_timeout

        try:
            logger.info(f"Fetching data from {url}")

            # request the excel file from the central bank
            with requests.get(url, timeout=timeout ) as response:
                response.raise_for_status()
                # save file to disk as raw data
                with open(f"data/source_file_{datetime.now().strftime('%Y-%m-%d')}.xlsx", "wb") as f:
                    f.write(response.content)
                
                # read the file using polars
                table = pl.read_excel(
                    response.content,
                    read_options={
                        "header_row": 2,

                    })

            columns = [
                'Año', 'Mes', 'Día', 'DOLAR AUSTRALIANO', 'REAL BRASILENO',
                'DOLAR CANADIENSE', 'FRANCO SUIZO', 'YUAN CHINO',
                'DERECHO ESPECIAL DE GIRO', 'CORONA DANESA', 'EURO',
                'LIBRA ESTERLINA', 'YEN JAPONES', 'CORONA NORUEGA',
                'LIBRA ESCOCESA', 'CORONA SUECA', 'DOLAR ESTADOUNIDENSE', 
                '*BOLIVAR FUERTE VENEZOLANO'
            ]

            # validate columns are present
            missing_columns = [col for col in columns if col not in table.columns]
            if missing_columns:
                table.write_csv(f"data/invalid_data_{datetime.now().strftime('%Y-%m-%d')}.csv")
                logger.error(f"Missing columns in data: {missing_columns}")
                return None
            
            table.write_parquet(f"data/raw_data_{datetime.now().strftime('%Y-%m-%d')}.parquet")
            return table

        except requests.RequestException as e:
            logger.error(f"Failed to fetch data: {e}")
            return None


if __name__ == "__main__":
    ingestor = CentralBankIngestor()
    data = ingestor.fetch_data()
    if data is not None:
        print("Data fetched successfully:")
        print(data.tail())
    else:
        print("Failed to fetch data.")