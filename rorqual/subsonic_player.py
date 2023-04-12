from __future__ import annotations

import asyncio
from typing import Literal, Sequence, cast

import httpx
from mpv import MPV, MpvEvent, MpvEventID

from subsonic.subsonic_rest_api import Child

from .callbacks import CallbackList
from .stream_manager import Buffer, StreamManager

PlaybackState = Literal["stopped", "playing", "paused"]


class SubsonicPlayer:
    PROTOCOL = "subsonic"

    def __init__(self, streams: StreamManager, loop: asyncio.AbstractEventLoop) -> None:
        self._streams = streams
        self._loop = loop

        self.time_position_callbacks = CallbackList[float | None]()
        self.playlist_position_callbacks = CallbackList[int | None]()
        self.playback_state_callbacks = CallbackList[PlaybackState]()
        self.playlist_content_callbacks = CallbackList[list[Child]]()

        self._playlist = list[Child]()
        self._playlist_position: int | None = None

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

    def _url(self, track: Child) -> str:
        return f"{self.PROTOCOL}://{track.id}"

    @property
    def playlist(self) -> Sequence[Child]:
        return self._playlist

    def playlist_clear(self) -> None:
        self.stop()
        self._streams.abort_prefetching()
        self._playlist = []
        self._playlist_position = None
        self.playlist_content_callbacks(self._playlist)

    def playlist_append(self, tracks: list[Child]) -> None:
        self._playlist += tracks
        self.playlist_content_callbacks(self._playlist)

    @property
    def current_track(self) -> Child | None:
        if self._playlist_position is None:
            return None

        return self._playlist[self._playlist_position]

    @property
    def next_track(self) -> Child | None:
        if self._playlist_position is None or self._playlist_position + 1 not in range(0, len(self._playlist)):
            return None

        return self._playlist[self._playlist_position + 1]

    @property
    def previous_track(self) -> Child | None:
        if self._playlist_position is None or self._playlist_position - 1 not in range(0, len(self._playlist)):
            return None

        return self._playlist[self._playlist_position - 1]

    @property
    def playlist_position(self) -> int | None:
        return self._playlist_position

    @property
    def playback_state(self) -> PlaybackState:
        if self.playlist_position is None:
            return "stopped"
        if self._mpv.pause:
            return "paused"

        return "playing"

    def play(self, playlist_position: int) -> None:
        self._playlist_position = playlist_position
        self._mpv.loadfile(self._url(cast(Child, self.current_track)), mode="replace")

        self.playback_state_callbacks("playing")
        self.playlist_position_callbacks(self._playlist_position)

        if self.next_track is not None:
            self._mpv.playlist_append(self._url(self.next_track))

    def play_next(self) -> None:
        if self.next_track is not None and self._playlist_position is not None:
            self.play(self._playlist_position + 1)

    def play_previous(self) -> None:
        if self.previous_track is not None and self._playlist_position is not None:
            self.play(self._playlist_position - 1)

    def toggle_paused(self) -> None:
        if self.playback_state == "stopped":
            return

        new_state = not self._mpv.pause
        self._mpv.pause = new_state
        self.playback_state_callbacks("paused" if new_state else "playing")

    def stop(self) -> None:
        self._mpv.stop(keep_playlist=False)
        self.playback_state_callbacks("stopped")

    def _playlist_advance(self) -> None:
        if self._playlist_position is not None:
            self._playlist_position += 1
        else:
            self._playlist_position = 0

        self._mpv.playlist_clear()

        if self.next_track is not None:
            self._mpv.playlist_append(self._url(self.next_track))

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
                            self._playlist_advance()
                        case -1:
                            self.playback_state_callbacks("stopped")
                            self._playlist_position = None
                    self.playlist_position_callbacks(self._playlist_position)

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
