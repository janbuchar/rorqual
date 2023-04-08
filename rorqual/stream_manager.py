import asyncio
from typing import Literal, NoReturn

from .callbacks import CallbackList
from .config import Config
from .subsonic_client import Buffer, SubsonicClient

FetchingState = Literal["pending", "fetching", "done"]


class StreamManager:
    def __init__(self, subsonic: SubsonicClient, config: Config) -> None:
        self.fetching_state_callbacks = CallbackList[str, FetchingState]()

        self._config = config
        self._subsonic = subsonic

        self._buffers = dict[str, Buffer]()
        self._queue = asyncio.Queue[str]()
        self._tasks = [asyncio.create_task(self._worker()) for _ in range(self._config.prefetch_worker_count)]

    async def _worker(self) -> NoReturn:
        while True:
            id = await self._queue.get()
            self.fetching_state_callbacks(id, "fetching")
            await self._subsonic.stream(id, self._buffers[id])
            self.fetching_state_callbacks(id, "done")

    def fetch(self, id: str) -> Buffer:
        if id not in self._buffers:
            self.fetching_state_callbacks(id, "pending")
            self._buffers[id] = Buffer()
            self._queue.put_nowait(id)

        return self._buffers[id]

    def abort_prefetching(self) -> None:
        for task in self._tasks:
            task.cancel()

        self._queue = asyncio.Queue[str]()
        self._tasks = [asyncio.create_task(self._worker()) for _ in range(self._config.prefetch_worker_count)]
