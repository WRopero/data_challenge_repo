from queue import Queue
from threading import Thread
import logging
import time
from components.database_manager import DatabaseManager
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class GenerateWorker(Thread):
    """
   To generate the workers that will insert the data to the database.
    """
    def __init__(self, q: Queue, thread_id, env, db_url, max_attempt, model):
        self.queue = q
        self.thread_id = thread_id
        self.env = env
        self.max_attempt = max_attempt
        self.db_manager = DatabaseManager(db_url)
        self.model = model
        super().__init__()

    def run(self) -> None:
        
        while True:
            target, attempt = self.queue.get(timeout=3)
            try:
                if target is None:
                    self.queue.task_done()
                    break

                logging.info(f"Thread {self.thread_id} is loading data for attempt {attempt}")
                self.db_manager.load_data(model=self.model, dataframe=target)
                self.queue.task_done()
                logging.info(f"new queue size: {self.queue.qsize()}")


            except Exception as e:
                if attempt < self.max_attempt:
                    logging.warning(f"Issue loading data: {e}")
                    self.queue.put((target, attempt + 1))
                    self.queue.task_done()
                else:
                    logging.critical(f"Final attempt failed at uploading data: {e}")

                
