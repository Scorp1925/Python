import time
from contextlib import contextmanager

@contextmanager
def timer():
    start_time = time.time()
    yield
    end_time = time.time()
    print(f"Elapsed time: {end_time-start_time:.2f} seconds")

with timer():
    time.sleep(2)

    