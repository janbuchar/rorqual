from __future__ import annotations

import asyncio

import httpx
from mpv import MPV

from .subsonic_client import Buffer, SubsonicClient


class SubsonicPlayer:
    PROTOCOL = "subsonic"

    def __init__(self, client: SubsonicClient, loop: asyncio.AbstractEventLoop) -> None:
        self.client = client
        self.loop = loop
        self.mpv = MPV()
        self.mpv.register_stream_protocol(self.PROTOCOL, self._open)

    def _open(self, url: str) -> SubsonicStreamFrontend:
        parsed_url = httpx.URL(url)

        if parsed_url.scheme != self.PROTOCOL:
            raise ValueError("Unsupported protocol")

        buffer = Buffer()
        task = self.loop.create_task(self.client.stream(parsed_url.host, buffer))
        return SubsonicStreamFrontend(buffer, task, self.loop)


class SubsonicStreamFrontend:
    """
    Bridges the MPV stream interface (thread-based) and the rest of the app (coroutine-based)
    """

    def __init__(self, buffer: Buffer, stream_task: asyncio.Task, loop: asyncio.AbstractEventLoop) -> None:
        self.buffer = buffer
        self.stream_task = stream_task
        self.loop = loop

    def read(self, size: int) -> bytes:
        return asyncio.run_coroutine_threadsafe(self.buffer.read(size), self.loop).result()

    def seek(self, pos: int) -> int:
        return self.buffer.seek(pos)

    def close(self) -> None:
        self.stream_task.cancel()
