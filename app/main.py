from utils.read_yaml_file import yaml_to_dict
from utils.manage_database_models import action_db_tables
from utils.manage_workers_and_queue import manage_workers_and_queue
from utils.get_sql import get_questions_handler
from utils.debuggers import debug_time
import logging
from fastapi import FastAPI

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

config = yaml_to_dict()


app = FastAPI()


@app.get("/")
def read_root():
    """
    Root API
    """
    return {"response": "This is a migration API!"}


@app.post("/create_tables")
def create_tables():
    """
    Create the tables declared as models in the MySQL database

    The order to create the tables because of dependencies is:
    1. jobs
    2. departments
    3. hired_employees

    If you do nto doit in th eorder, the tables will not be created
    """
    try: 
        table_names = action_db_tables(config['DATABASE_URL'])

        return {"logger": f"Tables created in database: {config['DATABASE_URL'].split('/')[-1]}",
                "tables_created": table_names}
    except Exception as e:
        return {"error": f"Error creating tables: {e}"}


@app.post("/drop_tables")
def drop_tables():
    """
    Drop the tables declared as models in the MySQL database
    """
    
    table_names = action_db_tables(config['DATABASE_URL'], type_action="drop")

    return {"logger": f"Tables dropped in database: {config['DATABASE_URL'].split('/')[-1]}",
            "tables_dropped": table_names}


@app.post("/load_data/{filename}")
def load_data(filename: str, thread_count: int, chunk_size: int, env: str):
    """
    Load the data from the file to the database
    :param filename: Name of the file
    :param thread_count: Number of threads
    :param chunk_size: Size of the chunk
    :param env: Environment

    """

    try:
        logger = manage_workers_and_queue(filename=filename, 
                            chunk_size=chunk_size, 
                            thread_count=thread_count, 
                            db_url=config['DATABASE_URL'], 
                            env=env)
        return logger
    except Exception as e:
        return {"error": f"Error loading data: {e}"}
    

@app.get("/get_questions/{question_file_name}")
def get_questions(file_name: str):
    """
    Get the questions from the SQL file
    :param file_name: Name of the SQL file with th eQuestion Resolved

    Filename Question 1: USe *question_1* as the file name
    Filename Question 2: USe *question_2* as the file name

    Question 1: Number of employees hired for each job and department in 2021 divided by quarter. The table must be ordered alphabetically by department and job.
    Question 2: List of ids, name and number of employees hired of each department that hired more employees than the mean of employees hired in 2021 for all the departments, ordered by the number of employees hired (descending).

    """
    try:
        result = get_questions_handler(db_url=config['DATABASE_URL'], sql_name=file_name)
        return {"result": result}
    except Exception as e:
        return {"error": f"Error loading query: {e}"}