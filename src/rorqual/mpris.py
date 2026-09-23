import asyncio
from typing import cast, override

from mpris_server.adapters import MprisAdapter
from mpris_server.base import DbusObj, Microseconds, NoTrack, PlayState, Track
from mpris_server.enums import LoopStatus
from mpris_server.events import EventAdapter
from mpris_server.mpris.metadata import Metadata, MetadataObj, ValidMetadata, get_dbus_metadata
from mpris_server.server import Server

from subsonic.subsonic_rest_api import Child

from .cover_manager import CoverManager
from .subsonic_player import LoopMode, PlaybackState, SubsonicPlayer

LOOP_STATUSES: dict[LoopStatus, LoopMode] = {
    LoopStatus.NONE: "none",
    LoopStatus.TRACK: "track",
    LoopStatus.PLAYLIST: "playlist",
}


class RorqualMprisAdapter(MprisAdapter):
    def __init__(self, player: SubsonicPlayer, cover_manager: CoverManager):
        super().__init__("Rorqual")
        self.player = player
        self.cover_manager = cover_manager
        self.loop = asyncio.get_running_loop()

    # RootAdapter
    @override
    def can_quit(self) -> bool:
        return False

    @override
    def can_raise(self) -> bool:
        return False

    @override
    def can_fullscreen(self) -> bool:
        return False

    @override
    def has_tracklist(self) -> bool:
        return True

    # PlayerAdapter
    @override
    def can_control(self) -> bool:
        return True

    def _track_id(self, position: int) -> DbusObj:
        return cast(DbusObj, f"/track/{self.player.entry_ids[position]}")

    def _position_of(self, track_id: DbusObj) -> int | None:
        return next(
            (position for position in range(len(self.player.playlist)) if self._track_id(position) == track_id), None
        )

    def _metadata(self, position: int) -> MetadataObj:
        track = self.player.playlist[position]
        cover_url = self.cover_manager.get_cover_url(track)
        if cover_url is None:
            asyncio.run_coroutine_threadsafe(self.cover_manager.fetch_cover(track), self.loop)

        return MetadataObj(
            track_id=self._track_id(position),
            length=(track.duration or 0) * 10**6,
            title=track.title,
            album=track.album,
            art_url=cover_url,
            track_number=track.track,
            disc_number=track.disc_number,
            artists=[track.artist] if track.artist else [],
            album_artists=[track.artist] if track.artist else [],
        )

    @override
    def metadata(self) -> ValidMetadata:
        if self.player.playlist_position is None:
            return MetadataObj(track_id=NoTrack)

        return self._metadata(self.player.playlist_position)

    @override
    def get_current_track(self) -> Track:
        metadata = cast(MetadataObj, self.metadata())
        return Track(track_id=cast(DbusObj, metadata.track_id))  # pyright: ignore[reportUnknownMemberType]

    @override
    def get_current_position(self) -> Microseconds:
        return int((self.player.time_position or 0) * 10**6)

    @override
    def get_playstate(self) -> PlayState:
        if self.player.playback_state == "stopped":
            return PlayState.STOPPED

        if self.player.playback_state == "paused":
            return PlayState.PAUSED

        return PlayState.PLAYING

    @override
    def can_go_next(self) -> bool:
        return self.player.next_track is not None

    @override
    def next(self) -> None:
        self.player.play_next()

    @override
    def can_go_previous(self) -> bool:
        return self.player.previous_track is not None

    @override
    def previous(self):
        self.player.play_previous()

    @override
    def can_play(self) -> bool:
        return len(self.player.playlist) > 0

    @override
    def can_pause(self) -> bool:
        return self.can_play()

    @override
    def pause(self) -> None:
        if self.player.playback_state == "playing":
            self.player.toggle_paused()

    @override
    def resume(self) -> None:
        if self.player.playback_state == "paused":
            self.player.toggle_paused()

    @override
    def stop(self) -> None:
        self.player.stop()

    @override
    def play(self) -> None:
        if self.player.playback_state == "stopped" and self.player.playlist:
            self.player.play(0)

    @override
    def can_seek(self) -> bool:
        return True

    @override
    def seek(self, time: Microseconds, track_id: DbusObj | None = None) -> None:
        if track_id is not None and track_id != self.get_current_track().track_id:
            return

        self.player.seek(time / 10**6)

    @override
    def is_repeating(self) -> bool:
        return self.player.loop_mode != "none"

    @override
    def set_repeating(self, value: bool) -> None:
        self.player.loop_mode = "playlist" if value else "none"

    @override
    def is_playlist(self) -> bool:
        return self.player.loop_mode == "playlist"

    @override
    def set_loop_status(self, value: LoopStatus) -> None:
        self.player.loop_mode = LOOP_STATUSES[value]

    @override
    def get_shuffle(self) -> bool:
        return self.player.shuffled

    @override
    def set_shuffle(self, value: bool) -> None:
        self.player.shuffled = value

    # TrackListAdapter
    @override
    def can_edit_tracks(self) -> bool:
        return False

    @override
    def get_tracks(self) -> list[DbusObj]:
        return [self._track_id(position) for position in range(len(self.player.playlist))]

    @override
    def get_tracks_metadata(self, track_ids: list[DbusObj]) -> list[Metadata]:
        positions = (self._position_of(track_id) for track_id in track_ids)
        return [get_dbus_metadata(self._metadata(position)) for position in positions if position is not None]

    @override
    def go_to(self, track_id: DbusObj) -> None:
        position = self._position_of(track_id)
        if position is not None:
            self.player.play(position)


class RorqualEventAdapter(EventAdapter):
    def __init__(self, adapter: RorqualMprisAdapter, mpris_server: Server):
        super().__init__(mpris_server.root, mpris_server.player, None, mpris_server.tracklist)

        self.adapter = adapter
        adapter.player.playback_state_callbacks.register(self.playback_state_changed)
        adapter.player.playlist_position_callbacks.register(self.track_changed)
        adapter.player.playlist_content_callbacks.register(self.playlist_changed)
        adapter.player.seek_callbacks.register(self.seeked)
        adapter.player.options_callbacks.register(self.on_options)
        adapter.cover_manager.cover_fetched_callbacks.register(self.on_title)

    def playback_state_changed(self, _state: PlaybackState) -> None:
        self.on_playpause()

    def track_changed(self, _position: int | None) -> None:
        self.on_playback()
        self.on_options()

    def playlist_changed(self, _tracks: list[Child]) -> None:
        self.on_list_replaced(self.adapter.get_tracks(), self.adapter.get_current_track().track_id)

    def seeked(self, position: float) -> None:
        self.on_seek(int(position * 10**6))
