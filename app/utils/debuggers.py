import time
from functools import wraps

def debug_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs) 
        end_time = time.time()
        time_taken = end_time - start_time
        print(f"{func.__name__} took {time_taken:.4f} seconds to finish.")
        return result
    return wrapper