import time
import logging

i=1

while True:
    time.sleep(5)
    logging.warning(f"Hello from the Python Container! {i}")
    i += 1