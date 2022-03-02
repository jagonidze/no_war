import logging
import socket
from urllib.parse import urlparse

import pandas as pd
import requests


class Targets:
    def __init__(self, url: str):
        self.targets = self._get_targets(url)
        logging.info("INIT TARGETS")

    def _get_targets(self, url) -> list[str]:
        req = requests.get(url)
        dataframe = pd.read_html(req.text)[0]
        targets = list()
        for _, row in dataframe.iterrows():
            for target in self._get_url(row):
                targets.append(target)
        return targets

    def _get_url(self, row: dict):
        for item in row.items():
            if type(item[1]) == str:
                try:
                    url = urlparse(item[1])
                    if url.netloc:
                        target_ip = {
                            "url": url.netloc,
                            "ip": socket.gethostbyname(url.netloc),
                        }
                    else:
                        target_ip = None
                        logging.info(f"IS NO TARGET {item[1]}")
                    if target_ip:
                        logging.info(f"GET TARGET {item[1]}")
                        yield target_ip
                except Exception as ex:
                    logging.info(f"{item[1]} HAS {ex}")

    def __getitem__(self, index):
        return self.targets[index]
    
    def __len__(self):
         return len(self.targets)
