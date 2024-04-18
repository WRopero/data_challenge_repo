import os
import logging
from components.database_manager import DatabaseManager

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def open_sql_file(sql_name: str):
    """
    Open a sql file and print the content
    :param sql_name: Name of the sql file

    """
    try:
        
        path_to_file =  os.path.join(os.path.dirname(__file__), 
                                 "..","config","sql", f"{sql_name}.sql")
        with open(path_to_file, 'r') as sql_file:
            sql_query = sql_file.read()
            # Do something with the SQL query
            return sql_query
    except FileNotFoundError:
        logging.critical(f"File '{sql_name}' not found.")

def get_questions_handler(  db_url: str, sql_name: str):
    """
    Get the questions from the sql file
    :param db_url: Database URL
    :param sql_name: Name of the sql file
    """
    query = open_sql_file(sql_name)
    db_manager = DatabaseManager(db_url)
    result_query = db_manager.execute_query(query)
    return result_query
