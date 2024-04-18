from utils.read_yaml_file import yaml_to_dict
from utils.manage_database_models import create_db_tables
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

config = yaml_to_dict()


create_db_tables(config['DATABASE_URL'])

logging.info(f"Config loaded: {config}")




# from fastapi import FastAPI

# app = FastAPI()

# @app.get("/")
# def read_root():
#     return {"Hello": "World"}

# if __name__ == "__main__":