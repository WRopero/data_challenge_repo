from queue import Queue
from threading import Thread
import logging
import time
from components.generate_final_sql_files import GenerateFinalSQLFiles
from tools.scrubber.utils.run_on_bigquery import run_and_store_log_query_results   
from utils.read_sql_files import get_sql_template
from utils.upload_metadata_data_to_bq import upload_metadata_data_to_bq
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class GenerateWorker(Thread):
    """
    Worker class to generate the final SQL files and run the anonymization process
    """
    def __init__(self, q: Queue, thread_id, env, max_attempt=5):
        self.table_queue = q
        self.thread_id = thread_id
        self.env = env
        self.max_attempt = max_attempt

        super().__init__()


    def run(self) -> None:

        while True:
            target_tables, attempt = self.table_queue.get(timeout=3)

            if target_tables is None:
                self.table_queue.task_done()
                break

            # try: 
            generate_final_sql_files = GenerateFinalSQLFiles(self.project_id, self.sql_template, target_tables)
            
            generate_final_sql_files.get_schemas()      
            dict_pi_rules = generate_final_sql_files.get_dict_with_pi_rules_mapping()
            path = generate_final_sql_files.trigger_sql_files_with_anon_functions(dict_pi_rules, 
                                        env=self.env, thread_id=self.thread_id)            
            
            sql_query = get_sql_template(sql_file_name=path[1])
            folder_path = path[0].replace("sql", "logs")
            sql_query = path[2]

            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            target_tables_dict = target_tables.to_dict("records")

            #Running dry run first            
            result_run_dry = run_and_store_log_query_results(project_id =self.project_id, 
                                                                    query = sql_query,
                                                                    path = folder_path, 
                                                                    thread_id=self.thread_id,
                                                                    target_table_data=target_tables_dict,
                                                                    type_run='dry_run')
            dry_run_status = result_run_dry[0]
            
            if dry_run_status != "DONE":
                logging.warning("The dry run failed \n")
            elif dry_run_status == "DONE":
                logging.info("The dry run was successful running PERSISTED QUERY ")   
                result_run = run_and_store_log_query_results(project_id =self.project_id, 
                                                                    query = sql_query,
                                                                    path = folder_path, 
                                                                    thread_id=self.thread_id,
                                                                    target_table_data=target_tables_dict,
                                                                    type_run='persisted_query')
                persisted_status = result_run[0]
                job_id = result_run[1]
                
                # Check if the job is done
                if persisted_status in ["DONE", "RUNNING", "PENDING"] :
                    logging.info(f"The persisted query is {persisted_status}. Storing the job id.")    
                    upload_metadata_data_to_bq(target_tables, job_id, persisted_status, sql_query)
                    
                    # Store the job id in the logging table
                else:
                    logging.warning("The persisted query failed or is in an unexpected state: %s", persisted_status)
                        #add logic to update the logging table with the status of the anonymization

            self.table_queue.task_done()
            # except Exception as e:
            #     log_error = "\n ".join(list(map(target_tables.to_dict("records")[0].get, 
            #                                     target_tables.to_dict("records")[0].keys())))
            #     # catch all exceptions and will attempt again up to the designated maximum
            #     if attempt < self.max_attempt:

            #         logging.warning("\n Issue in table_id: %s \n", log_error )
            #         self.table_queue.put((target_tables, attempt + 1))
            #         self.table_queue.task_done()
                    
            #     else:
            #         logging.critical("Final attempt failed at uploading %s", log_error)
            #         self.table_queue.task_done()
            #         raise e