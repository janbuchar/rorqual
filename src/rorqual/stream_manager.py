import asyncio
from collections import deque
from collections.abc import Iterable
from typing import Literal, NoReturn, cast
from weakref import WeakValueDictionary

from .caching import BlobCache
from .callbacks import CallbackList
from .config import PrefetchingConfig
from .subsonic_client import Buffer, SubsonicClient

type FetchingState = Literal["pending", "fetching", "done"]
type StreamId = str


class StreamManager:
    def __init__(self, subsonic: SubsonicClient, config: PrefetchingConfig) -> None:
        self.fetching_state_callbacks = CallbackList[StreamId, FetchingState]()

        self._config = config
        self._subsonic = subsonic
        self._cache = BlobCache("audio", config.audio_cache_size)

        self._buffers = WeakValueDictionary[StreamId, Buffer]()
        self._queue_condition = asyncio.Condition()
        self._queue = deque[StreamId]()

        self._tasks = list[asyncio.Task]()
        self._task_streams = dict[asyncio.Task, StreamId]()
        self._respawn_workers(keep_active=False)

    async def _worker(self) -> NoReturn:
        while True:
            if len(self._queue) == 0:
                async with self._queue_condition:
                    await self._queue_condition.wait()
                continue

            id = self._queue.popleft()
            buffer = self._buffers.setdefault(id, Buffer())

            task = cast(asyncio.Task, asyncio.current_task())
            self._task_streams[task] = id

            self.fetching_state_callbacks(id, "fetching")
            await self._subsonic.stream(id, buffer)
            self.fetching_state_callbacks(id, "done")
            self._cache.store(id, self._buffers[id].data)

            del self._task_streams[task]

    def _respawn_workers(self, *, keep_active: bool) -> None:
        for task in self._tasks:
            if not keep_active or self._task_streams.get(task) not in self._buffers:
                task.cancel()
                self._tasks.remove(task)

        if not keep_active:
            self._task_streams.clear()

        for _ in range(self._config.worker_count - len(self._tasks)):
            self._tasks.append(asyncio.create_task(self._worker()))

    async def prefetch(self, ids: Iterable[StreamId]) -> None:
        async with self._queue_condition:
            self._queue.clear()
            self._respawn_workers(keep_active=True)

            for id in ids:
                if id in self._cache:
                    self.fetching_state_callbacks(id, "done")
                    continue

                if id in self._buffers:
                    self.fetching_state_callbacks(id, "fetching")
                    continue

                self.fetching_state_callbacks(id, "pending")
                if id not in self._queue:
                    self._queue.append(id)

            self._queue_condition.notify_all()

    def abort_all_streams(self) -> None:
        self._queue.clear()
        self._respawn_workers(keep_active=False)

    async def fetch(self, id: StreamId) -> Buffer:
        if id in self._buffers:
            return self._buffers[id]

        cached_data = self._cache.read(id)
        if cached_data is not None:
            self.fetching_state_callbacks(id, "done")
            buffer = Buffer()
            buffer.allocate(len(cached_data))
            buffer.write(cached_data)
            return buffer

        if id not in self._buffers:
            self.fetching_state_callbacks(id, "pending")

            async with self._queue_condition:
                self._queue.append(id)
                self._queue_condition.notify_all()

        return self._buffers.setdefault(id, Buffer())
