import multiprocessing as mp
import threading
import time

def thread():
    while True:
        time.sleep(5)
        print("Inside thread")

x = threading.Thread(target=thread)

x.start()
while True:
    time.sleep(5)
    print("Number of processors: ", mp.cpu_count())