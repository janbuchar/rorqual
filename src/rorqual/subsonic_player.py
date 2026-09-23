from __future__ import annotations

import asyncio
from collections.abc import Sequence
from typing import Any, Literal, cast

from mpv import MPV, MpvEvent, MpvEventEndFile, MpvEventID

from subsonic.subsonic_rest_api import Child

from .callbacks import CallbackList
from .stream_manager import Buffer, StreamManager

PlaybackState = Literal["stopped", "playing", "paused"]
LoopMode = Literal["none", "track", "playlist"]


class SubsonicPlayer:
    """
    Playback control on top of mpv.

    mpv owns the playlist and all playback state - everything here is either a command sent to it
    or a mirror of an observed property, so the two can't drift apart.
    """

    PROTOCOL = "subsonic"

    def __init__(self, streams: StreamManager, loop: asyncio.AbstractEventLoop) -> None:
        self._streams = streams
        self._loop = loop

        self.time_position_callbacks = CallbackList[float | None]()
        self.playlist_position_callbacks = CallbackList[int | None]()
        self.playback_state_callbacks = CallbackList[PlaybackState]()
        self.playlist_content_callbacks = CallbackList[list[Child]]()
        self.seek_callbacks = CallbackList[float]()
        self.options_callbacks = CallbackList[[]]()

        self._tracks = dict[str, Child]()
        self._playlist = list[Child]()
        self._entry_ids = list[int]()

        # Mirrors of observed mpv properties, so that reads from the MPRIS thread don't hit mpv
        self._playlist_position: int | None = None
        self._paused = False
        self._time_position: float | None = None

        self._shuffled = False
        self._loop_mode: LoopMode = "none"

        self._mpv = MPV(
            audio_client_name="rorqual",
            title="${?media-title:${media-title}}${!media-title:No file}",
        )
        self._mpv.register_stream_protocol(self.PROTOCOL, self._open)
        self._mpv.observe_property("time-pos", self._handle_time_position)
        self._mpv.observe_property("pause", self._handle_pause)
        self._mpv.observe_property("playlist-pos", self._handle_playlist_position)
        self._mpv.register_event_callback(self._handle_end_file)

    def _open(self, url: str) -> SubsonicStreamFrontend:
        # Parsed by hand: a URL parser lowercases the host, and song ids are case sensitive
        scheme, separator, song_id = url.partition("://")

        if scheme != self.PROTOCOL or not separator:
            raise ValueError("Unsupported protocol")

        return SubsonicStreamFrontend(
            asyncio.run_coroutine_threadsafe(self._streams.fetch(song_id), self._loop).result(),
            self._loop,
        )

    def _url(self, track: Child) -> str:
        return f"{self.PROTOCOL}://{track.id}"

    def _sync_playlist(self) -> None:
        entries = cast(list[dict[str, Any]], self._mpv.playlist)
        self._playlist = [self._tracks[str(entry["filename"]).removeprefix(f"{self.PROTOCOL}://")] for entry in entries]
        self._entry_ids = [int(entry["id"]) for entry in entries]
        self.playlist_content_callbacks(self._playlist)

    @property
    def playlist(self) -> Sequence[Child]:
        return self._playlist

    @property
    def entry_ids(self) -> Sequence[int]:
        """mpv's playlist entry ids, positionally matching `playlist`. Stable across reordering."""
        return self._entry_ids

    def playlist_clear(self) -> None:
        self._mpv.stop()
        self._tracks.clear()
        self._sync_playlist()

    def playlist_append(self, tracks: list[Child]) -> None:
        for track in tracks:
            self._tracks[track.id] = track
            self._mpv.playlist_append(self._url(track))

        self._sync_playlist()

    @property
    def current_track(self) -> Child | None:
        if self._playlist_position is None:
            return None

        return self._playlist[self._playlist_position]

    def _adjacent_track(self, offset: int) -> Child | None:
        if self._playlist_position is None:
            return None

        position = self._playlist_position + offset
        if position not in range(len(self._playlist)):
            if self._loop_mode != "playlist":
                return None
            position %= len(self._playlist)

        return self._playlist[position]

    @property
    def next_track(self) -> Child | None:
        return self._adjacent_track(1)

    @property
    def previous_track(self) -> Child | None:
        return self._adjacent_track(-1)

    @property
    def playlist_position(self) -> int | None:
        return self._playlist_position

    @property
    def time_position(self) -> float | None:
        return self._time_position

    @property
    def playback_state(self) -> PlaybackState:
        if self._playlist_position is None:
            return "stopped"

        return "paused" if self._paused else "playing"

    @property
    def shuffled(self) -> bool:
        return self._shuffled

    @shuffled.setter
    def shuffled(self, value: bool) -> None:
        if value == self._shuffled:
            return

        # mpv only remembers one shuffle to undo, so unshuffling after appending tracks restores an approximation.
        # Keep our own ordering if that ever bites.
        if value:
            self._mpv.playlist_shuffle()
        else:
            self._mpv.playlist_unshuffle()

        self._shuffled = value
        self._sync_playlist()
        self.options_callbacks()

    @property
    def loop_mode(self) -> LoopMode:
        return self._loop_mode

    @loop_mode.setter
    def loop_mode(self, value: LoopMode) -> None:
        self._mpv.loop_file = "inf" if value == "track" else "no"
        self._mpv.loop_playlist = "inf" if value == "playlist" else "no"
        self._loop_mode = value
        self.options_callbacks()

    def play(self, playlist_position: int) -> None:
        self._mpv.pause = False
        self._mpv.playlist_play_index(playlist_position)

    def play_next(self) -> None:
        if self.next_track is not None:
            self._mpv.playlist_next()

    def play_previous(self) -> None:
        if self.previous_track is not None:
            self._mpv.playlist_prev()

    def toggle_paused(self) -> None:
        if self.playback_state == "stopped":
            return

        self._mpv.pause = not self._paused

    def seek(self, position: float) -> None:
        if self.playback_state == "stopped":
            return

        self._mpv.seek(position, reference="absolute")
        self.seek_callbacks(position)

    def stop(self) -> None:
        self._mpv.stop(keep_playlist=True)

    def _handle_time_position(self, _name: str, position: float | None) -> None:
        self._time_position = position
        self.time_position_callbacks(position)

    def _handle_pause(self, _name: str, paused: bool) -> None:
        self._paused = paused
        self.playback_state_callbacks(self.playback_state)

    def _handle_playlist_position(self, _name: str, position: int | None) -> None:
        self._playlist_position = position if position is not None and position >= 0 else None
        self.playlist_position_callbacks(self._playlist_position)
        self.playback_state_callbacks(self.playback_state)

    def _handle_end_file(self, event: MpvEvent) -> None:
        if event.event_id.value != MpvEventID.END_FILE:
            return

        end_file = cast(MpvEventEndFile, event.data)
        if end_file.reason != MpvEventEndFile.ERROR:
            return

        # Left alone, mpv would burn through the rest of the playlist one failure at a time
        self._mpv.stop(keep_playlist=True)

        entry_id = int(end_file.playlist_entry_id)
        if entry_id in self._entry_ids:
            self._streams.report_failure(self._playlist[self._entry_ids.index(entry_id)].id)


class SubsonicStreamFrontend:
    """
    Bridges the MPV stream interface (thread-based) and the rest of the app (coroutine-based)
    """

    def __init__(self, buffer: Buffer, loop: asyncio.AbstractEventLoop) -> None:
        self.buffer = buffer
        self.loop = loop

    @property
    def size(self) -> int | None:
        if not self.buffer.started.is_set():
            return None
        return len(self.buffer.data)

    def read(self, size: int) -> bytearray:
        return asyncio.run_coroutine_threadsafe(self.buffer.read(size), self.loop).result()

    def seek(self, pos: int) -> int:
        return self.buffer.seek(pos)
