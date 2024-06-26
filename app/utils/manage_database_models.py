from components.database_manager import DatabaseManager
from models.database_models import MODELS_LIST
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def action_db_tables(db_url, type_action="create"):

    logging.info(f"Creating tables in database: {db_url.split('/')[-1]}")
    db_manager = DatabaseManager(db_url)
    if type_action == "drop":
        db_manager.drop_tables(MODELS_LIST)
    db_manager.create_tables(MODELS_LIST)
    table_names = ", ".join([model.__tablename__ for model in MODELS_LIST])
    return table_names