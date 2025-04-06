import asyncio
from datetime import datetime, timedelta
from typing import Any, TypeVar, cast
from mpris_server.enums import LoopStatus
from typing_extensions import override

from mpris_server.adapters import MprisAdapter
from mpris_server.base import PlayState, DbusObj, Microseconds, Track
from mpris_server.events import EventAdapter
from mpris_server.mpris.metadata import MetadataObj, ValidMetadata
from mpris_server.server import Server

from .cover_manager import CoverManager
from .subsonic_player import SubsonicPlayer


class RorqualMprisAdapter(MprisAdapter):
    def __init__(self, player: SubsonicPlayer, cover_manager: CoverManager):
        super().__init__("Rorqual")
        self.player = player
        self.cover_manager = cover_manager
        self.loop = asyncio.get_running_loop()

        self.time_position: float = 0

        self.player.time_position_callbacks.register(self.on_time_position_change)

    def on_time_position_change(self, position: float | None) -> None:
        self.time_position = position or 0

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
        return False

    # PlayerAdapter
    @override
    def can_control(self) -> bool:
        return True

    @override
    def metadata(self) -> ValidMetadata:
        if self.player.playlist_position is None or self.player.current_track is None:
            return MetadataObj(track_id="/track/none")

        track = self.player.current_track
        cover_url = self.cover_manager.get_cover_url(track)
        if cover_url is None:
            asyncio.run_coroutine_threadsafe(self.cover_manager.fetch_cover(track), self.loop)

        return MetadataObj(
            track_id=f"/track/{self.player.playlist_position}",
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
    def get_current_track(self) -> Track:
        metadata = cast(MetadataObj, self.metadata())
        return Track(track_id=cast(DbusObj, metadata.track_id)) # pyright: ignore[reportUnknownMemberType]

    @override
    def get_current_position(self) -> Microseconds:
        return int(self.time_position * (10**6))

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
        return self.player.current_track is not None

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

    def play_pause(self) -> None:
        if self.player.playback_state == "playing" or self.player.playback_state == "paused":
            self.player.toggle_paused()
        elif self.player.playback_state == "stopped" and len(self.player.playlist) > 0:
            self.player.play(0)

    @override
    def can_seek(self) -> bool:
        return True

    @override
    def seek(self, time: Microseconds, track_id: DbusObj | None = None):
        pass

    @override
    def is_repeating(self) -> bool:
        return False

    @override
    def set_repeating(self, value: bool) -> None:
        pass

    @override
    def is_playlist(self) -> bool:
        return False

    @override
    def set_loop_status(self, value: LoopStatus) -> None:
        pass

    @override
    def get_shuffle(self) -> bool:
        return False

    @override
    def set_shuffle(self, value: bool) -> None:
        pass

    # TrackListAdapter
    @override
    def can_edit_tracks(self) -> bool:
        return False

T = TypeVar('T')
def not_none(value: T | None) -> T:
    if value is None:
        raise ValueError("Received None")
    return value

class RorqualEventAdapter(EventAdapter):
    def __init__(self, subsonic: SubsonicPlayer, cover_manager: CoverManager, mpris_server: Server):
        super().__init__(mpris_server.root, mpris_server.player, None, None)

        self.subsonic = subsonic
        self.subsonic.time_position_callbacks.register(self.time_position_callback)
        self.subsonic.playback_state_callbacks.register(self.notify)
        self.subsonic.playlist_position_callbacks.register(self.notify)

        self.cover_manager = cover_manager
        self.cover_manager.cover_fetched_callbacks.register(self.notify)
        self.last_position_change_emission = datetime.utcnow()

    def time_position_callback(self, time_position: float | None):
        now = datetime.utcnow()
        if self.last_position_change_emission and now - self.last_position_change_emission < timedelta(seconds=0.5):
            return

        not_none(self.player).Seeked.emit((time_position or 0) * 10**6)
        self.emit_player_changes(["Position"])
        self.last_position_change_emission = now

    def notify(self, *args: Any, **kwargs: Any) -> None:
        self.on_player_all()
