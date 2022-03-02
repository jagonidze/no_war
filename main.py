import logging
import multiprocessing
import threading

from defs.port_filler import PortFiller
from defs.loader import Loader
from defs.targets import Targets

CPUS = multiprocessing.cpu_count()
URL = "https://docs.google.com/spreadsheets/d/1TlWTY9jxtyyb1H3AGt4QiQo17MGEUSE4LOl7vgynwxg/edit"


if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

    targes = Targets(URL)
    port_filler = PortFiller(targes)
    loader = Loader(targes)
    threads = list()
    for index in range(CPUS):
        x = threading.Thread(target=loader.start)
        threads.append(x)
        x.start()

    for index, thread in enumerate(threads):
        thread.join()
