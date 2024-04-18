from components.database_manager import DatabaseManager
from models.database_models import MODELS_LIST
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_db_tables(db_url):

    logging.info(f"Creating tables in database: {db_url.split('/')[-1]}")
    db_manager = DatabaseManager(db_url)
    db_manager.create_tables(MODELS_LIST)