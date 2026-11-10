import asyncio
import tempfile
from collections import deque
from collections.abc import Iterable
from pathlib import Path
from typing import Literal, NoReturn, cast
from weakref import WeakValueDictionary

from platformdirs import user_cache_dir

from .caching import BlobCache
from .callbacks import CallbackList
from .config import PrefetchingConfig
from .subsonic_client import Buffer, SubsonicClient

type FetchingState = Literal["pending", "fetching", "done", "failed"]
type StreamId = str


class StreamManager:
    def __init__(self, subsonic: SubsonicClient, config: PrefetchingConfig) -> None:
        self.fetching_state_callbacks = CallbackList[StreamId, FetchingState]()

        self._config = config
        self._subsonic = subsonic
        self._cache = BlobCache("audio", config.audio_cache_size)
        # Next to the cache, so that finished downloads can be renamed into it. Per process, removed on exit.
        self._staging = tempfile.TemporaryDirectory(prefix="partial-", dir=user_cache_dir("rorqual"))

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
            buffer = self._buffers.setdefault(id, Buffer(Path(self._staging.name)))

            task = cast(asyncio.Task, asyncio.current_task())
            self._task_streams[task] = id

            self.fetching_state_callbacks(id, "fetching")
            try:
                await self._subsonic.stream(id, buffer)
            finally:
                if not buffer.complete:
                    buffer.discard()

            if buffer.complete:
                assert buffer.path is not None
                self._cache.adopt(id, buffer.path)
                self.fetching_state_callbacks(id, "done")
            else:
                self.fetching_state_callbacks(id, "failed")

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

    def report_failure(self, id: StreamId) -> None:
        """Whatever we served for this stream turned out to be unplayable, so don't keep serving it."""
        self._cache.discard(id)
        self.fetching_state_callbacks(id, "failed")

    def cached_streams(self) -> set[StreamId]:
        return self._cache.keys()

    def abort_all_streams(self) -> None:
        self._queue.clear()
        self._respawn_workers(keep_active=False)

    async def fetch(self, id: StreamId) -> Buffer:
        if id in self._buffers:
            return self._buffers[id]

        cached_file = self._cache.open(id)
        if cached_file is not None:
            self.fetching_state_callbacks(id, "done")
            return Buffer.from_file(cached_file)

        async with self._queue_condition:
            # Checked under the lock: a second queue entry would stream into the same buffer again, under mpv's feet
            if id not in self._buffers and id not in self._queue:
                self.fetching_state_callbacks(id, "pending")
                self._queue.append(id)
                self._queue_condition.notify_all()

            return self._buffers.setdefault(id, Buffer(Path(self._staging.name)))
