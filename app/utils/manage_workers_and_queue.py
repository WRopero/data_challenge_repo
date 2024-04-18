from components.queue_manager import QueueManager
from components.threading_manager import GenerateWorker
import os
from models.database_models import ColumnEmployeesModel, ColumnDepartmentModel, ColumnJobsModel
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def manage_workers_and_queue(filename, chunk_size, thread_count, db_url, env='dev'):
    """
    Function to manage the workers and the queue
    :param file_path: Path to the file
    :param chunk_size: Size of the chunk
    :param thread_count: Number of threads
    """

    MODELS  = {
    'hired_employees': ColumnEmployeesModel,
    'departments': ColumnDepartmentModel,
    'jobs': ColumnJobsModel
    }

    worker_list = []

    file_path = os.path.join(os.path.dirname(__file__),"..", "source", f"{filename}.csv")
    model = MODELS.get(filename)
    col_names = [column.name for column in model.__table__.columns]
    queue_manager_objetcs = QueueManager(file_path, chunk_size).add_to_queue(col_names=col_names)
    queue_manager = queue_manager_objetcs[0]
    shunks = queue_manager_objetcs[1]
    if shunks <= 1:
        thread_count = shunks #if the shunks are = 1, then only 1 worker is needed
   

    for _ in range(thread_count):
        queue_manager.put((None,0)) 


    logging.info(f"Queue size: {queue_manager.qsize()}")

    for thread_i in range(thread_count):
        worker = GenerateWorker(q=queue_manager,
                                thread_id=thread_i + 1,
                                env=env,
                                db_url=db_url,
                                max_attempt=2, 
                                model=model)
        worker.daemon = True # Daemon threads will exit when the main thread exits
        worker.start()
        worker_list.append(worker)

    # Wait for all workers to finish
    for worker in worker_list:
        worker.join()
    
    return {"logger": f"Data loaded successfully to {filename} table!"}
