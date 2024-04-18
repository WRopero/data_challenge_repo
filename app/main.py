from utils.read_yaml_file import yaml_to_dict
from utils.manage_database_models import create_db_tables
from utils.manage_workers_and_queue import manage_workers_and_queue
import logging
from fastapi import FastAPI

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

config = yaml_to_dict()


app = FastAPI()


@app.get("/")
def read_root():
    return {"response": "This is a migration API!"}


@app.post("/create_tables")
def create_tables():
    
    table_names = create_db_tables(config['DATABASE_URL'])

    return {"logger": f"Tables created in database: {config['DATABASE_URL'].split('/')[-1]}",
            "tables_created": table_names}

@app.post("/load_data/{filename}")
def load_data(filename: str, thread_count: int, chunk_size: int, env: str):

    try:
        logger = manage_workers_and_queue(filename=filename, 
                            chunk_size=chunk_size, 
                            thread_count=thread_count, 
                            db_url=config['DATABASE_URL'], 
                            env=env)
        return logger
    except Exception as e:
        return {"logger": f"Error loading data: {e}"}






# # create_db_tables(config['DATABASE_URL'])
# # logging.info(f"Config loaded: {config}")









# # from fastapi import FastAPI

# # app = FastAPI()

# # @app.get("/")
# # def read_root():
# #     return {"Hello": "World"}

# # if __name__ == "__main__":