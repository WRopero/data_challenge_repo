import queue
import logging
import pandas as pd

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class QueueManager:
    def __init__(self, file_path, chunk_size=1000):
        self.queue = queue.Queue()
        self.file_path = file_path
        self.chunk_size = chunk_size

    def add_to_queue(self, col_names=None):        
        logging.info(f"Adding {self.file_path} to queue")

        count = 0
        
        for chunk in pd.read_csv(self.file_path, chunksize=self.chunk_size, sep=',',names=col_names):
            count += 1
            self.queue.put((chunk, 0))
            logging.info(f"Chunk {count} added to queue")        

        
        logging.info(f"Data added to queue, queue size: {self.queue.qsize()}")
        return self.queue, count
    
    def clear_queue(self):
        self.queue.clear()
        print("Queue cleared, queue size:", self.queue.qsize())