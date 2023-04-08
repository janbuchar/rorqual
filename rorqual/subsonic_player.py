from __future__ import annotations

import asyncio
from typing import Literal

import httpx
from mpv import MPV, MpvEvent, MpvEventID

from .callbacks import CallbackList
from .stream_manager import Buffer, StreamManager

PlaybackState = Literal["stopped", "playing", "paused"]


class SubsonicPlayer:
    PROTOCOL = "subsonic"

    def __init__(self, streams: StreamManager, loop: asyncio.AbstractEventLoop) -> None:
        self._streams = streams
        self._loop = loop

        self.time_position_callbacks = CallbackList[float | None]()
        self.next_track_start_callbacks = CallbackList[[]]()
        self.playback_state_callbacks = CallbackList[PlaybackState]()

        self._mpv = MPV()
        self._mpv.register_stream_protocol(self.PROTOCOL, self._open)
        self._mpv.register_event_callback(self.handle_event)
        self._mpv.observe_property("time-pos", self.dummy_property_handler)
        self._mpv.observe_property("pause", self.dummy_property_handler)
        self._mpv.observe_property("filename", self.dummy_property_handler)
        self._mpv.observe_property("playlist-current-pos", self.dummy_property_handler)

    def _open(self, url: str) -> SubsonicStreamFrontend:
        parsed_url = httpx.URL(url)

        if parsed_url.scheme != self.PROTOCOL:
            raise ValueError("Unsupported protocol")

        return SubsonicStreamFrontend(self._streams.fetch(parsed_url.host), self._loop)

    def _prefix_id(self, id: str) -> str:
        return f"{self.PROTOCOL}://{id}"

    def play(self, id: str) -> None:
        self._mpv.loadfile(self._prefix_id(id), mode="replace")
        self.playback_state_callbacks("playing")

    def set_next_track(self, id: str) -> None:
        self._mpv.playlist_clear()
        self._mpv.playlist_append(self._prefix_id(id))

    def toggle_paused(self) -> None:
        self._mpv.pause = not self._mpv.pause

    def stop(self) -> None:
        self._mpv.stop(keep_playlist=False)

    def handle_event(self, event: MpvEvent) -> None:
        match event.event_id.value:
            case MpvEventID.PROPERTY_CHANGE if event.data:
                if event.data.name == "time-pos":
                    self.time_position_callbacks(event.data.value)
                if event.data.name == "pause":
                    self.playback_state_callbacks("paused" if event.data.value else "playing")
                if event.data.name == "playlist-current-pos":
                    match event.data.value:
                        case 1:
                            self.next_track_start_callbacks()
                        case -1:
                            self.playback_state_callbacks("stopped")

    def dummy_property_handler(self, *args) -> None:
        pass


class SubsonicStreamFrontend:
    """
    Bridges the MPV stream interface (thread-based) and the rest of the app (coroutine-based)
    """

    def __init__(self, buffer: Buffer, loop: asyncio.AbstractEventLoop) -> None:
        self.buffer = buffer
        self.loop = loop

    def read(self, size: int) -> bytes:
        return asyncio.run_coroutine_threadsafe(self.buffer.read(size), self.loop).result()

    def seek(self, pos: int) -> int:
        return self.buffer.seek(pos)
