from core import get_ips, send_requests
import multiprocessing
import threading
import logging


CPUS = multiprocessing.cpu_count()


if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(
        format=format, 
        level=logging.INFO,
        datefmt="%H:%M:%S"
    )
    
    targes = get_ips('love.txt')
    threads = list()
    for index in range(CPUS):
        x = threading.Thread(target=send_requests, args=(targes,))
        threads.append(x)
        x.start()
    
    for index, thread in enumerate(threads):
        thread.join()