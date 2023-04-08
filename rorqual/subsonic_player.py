from __future__ import annotations

import asyncio
from typing import Any, Callable, Generic, ParamSpec

import httpx
from mpv import MPV, MpvEvent, MpvEventID

from .subsonic_client import Buffer, SubsonicClient

TArgs = ParamSpec("TArgs")


class CallbackList(Generic[TArgs]):
    def __init__(self) -> None:
        self.callbacks = list[Callable[TArgs, Any]]()

    def register(self, callback: Callable[TArgs, Any]) -> None:
        self.callbacks.append(callback)

    def __call__(self, *args: TArgs.args, **kwargs: TArgs.kwargs) -> Any:
        for callback in self.callbacks:
            callback(*args, **kwargs)


class SubsonicPlayer:
    PROTOCOL = "subsonic"

    def __init__(self, client: SubsonicClient, loop: asyncio.AbstractEventLoop) -> None:
        self.client = client
        self.loop = loop

        self._mpv = MPV()
        self._mpv.register_stream_protocol(self.PROTOCOL, self._open)
        self._mpv.register_event_callback(self.handle_event)
        self._mpv.observe_property("time-pos", self.dummy_property_handler)
        self._mpv.observe_property("pause", self.dummy_property_handler)
        self._mpv.observe_property("filename", self.dummy_property_handler)
        self._mpv.observe_property("playlist-current-pos", self.dummy_property_handler)

        self.time_position_callbacks = CallbackList[float | None]()
        self.next_track_start_callbacks = CallbackList[[]]()

        self._paused = False
        self._playing_track: str | None = None
        self._playlist = list[str]()

    def _open(self, url: str) -> SubsonicStreamFrontend:
        parsed_url = httpx.URL(url)

        if parsed_url.scheme != self.PROTOCOL:
            raise ValueError("Unsupported protocol")

        buffer = Buffer()
        task = self.loop.create_task(self.client.stream(parsed_url.host, buffer))
        return SubsonicStreamFrontend(buffer, task, self.loop)

    def _prefix_id(self, id: str) -> str:
        return f"{self.PROTOCOL}://{id}"

    def play(self, id: str) -> None:
        self._mpv.loadfile(self._prefix_id(id), mode="replace")

    def set_next_track(self, id: str) -> None:
        self._mpv.playlist_clear()
        self._mpv.playlist_append(self._prefix_id(id))

    def toggle_paused(self) -> None:
        self._mpv.pause = not self._paused

    @property
    def playing_track(self) -> str | None:
        return self._playing_track

    def handle_event(self, event: MpvEvent) -> None:
        match event.event_id.value:
            case MpvEventID.PROPERTY_CHANGE if event.data:
                if event.data.name == "time-pos" and self.time_position_callbacks:
                    self.time_position_callbacks(event.data.value)
                if event.data.name == "pause":
                    self._paused = event.data.value
                if event.data.name == "filename":
                    self._playing_track = event.data.value
                if event.data.name == "playlist-current-pos":
                    if event.data.value == 1:
                        self.next_track_start_callbacks()

    def dummy_property_handler(self, *args) -> None:
        pass


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
