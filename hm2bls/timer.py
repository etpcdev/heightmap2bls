import time

def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        res = func(*args, **kwargs)
        end_time = time.time()
        exec_time = end_time - start_time
        print(f"-> Done in {exec_time:.4f} seconds")
        return res
    return wrapper