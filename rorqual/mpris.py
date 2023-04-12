import asyncio
from typing import cast

from mpris_server.adapters import DbusObj, Microseconds, MprisAdapter, Track, ValidMetadata
from mpris_server.base import PlayState
from mpris_server.events import EventAdapter, Player, Root
from mpris_server.mpris.metadata import MetadataObj
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
    def can_quit(self) -> bool:
        return False

    def can_raise(self) -> bool:
        return False

    def can_fullscreen(self) -> bool:
        return False

    def has_tracklist(self) -> bool:
        return False

    # PlayerAdapter
    def can_control(self) -> bool:
        return True

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
            track_no=track.track,
            disc_no=track.disc_number,
            artists=[track.artist] if track.artist else [],
            album_artists=[track.artist] if track.artist else [],
        )

    def get_current_track(self) -> Track:
        metadata = cast(MetadataObj, self.metadata())
        return Track(track_id=metadata.track_id)

    def get_current_position(self) -> Microseconds:
        return int(self.time_position * (10**6))

    def get_playstate(self) -> PlayState:
        if self.player.playback_state == "stopped":
            return PlayState.STOPPED

        if self.player.playback_state == "paused":
            return PlayState.PAUSED

        return PlayState.PLAYING

    def can_go_next(self) -> bool:
        return self.player.next_track is not None

    def next(self) -> None:
        self.player.play_next()

    def can_go_previous(self) -> bool:
        return self.player.previous_track is not None

    def previous(self):
        self.player.play_previous()

    def can_play(self) -> bool:
        return self.player.current_track is not None

    def can_pause(self) -> bool:
        return self.can_play()

    def pause(self) -> None:
        if self.player.playback_state == "playing":
            self.player.toggle_paused()

    def resume(self) -> None:
        if self.player.playback_state == "paused":
            self.player.toggle_paused()

    def stop(self) -> None:
        self.player.stop()

    def play_pause(self) -> None:
        if self.player.playback_state == "playing" or self.player.playback_state == "paused":
            self.player.toggle_paused()
        elif self.player.playback_state == "stopped" and len(self.player.playlist) > 0:
            self.player.play(0)

    def can_seek(self) -> bool:
        return True

    def seek(self, time: Microseconds, track_id: DbusObj | None = None):
        pass

    def is_repeating(self) -> bool:
        return False

    def set_repeating(self, value: bool) -> None:
        pass

    def is_playlist(self) -> bool:
        return False

    def set_loop_status(self, value: bool) -> None:
        pass

    def get_shuffle(self) -> bool:
        return False

    def set_shuffle(self, value: bool) -> None:
        pass

    # TrackListAdapter
    def can_edit_tracks(self) -> bool:
        return False


class RorqualEventAdapter(EventAdapter):
    def __init__(self, subsonic: SubsonicPlayer, cover_manager: CoverManager, mpris_server: Server):
        super().__init__(mpris_server.player, mpris_server.root, None, None)

        self.subsonic = subsonic
        self.subsonic.time_position_callbacks.register(self.time_position_callback)
        self.subsonic.playback_state_callbacks.register(self.notify)
        self.subsonic.playlist_position_callbacks.register(self.notify)

        self.cover_manager = cover_manager
        self.cover_manager.cover_fetched_callbacks.register(self.notify)

    def time_position_callback(self, time_position: float | None):
        self.player.Seeked.emit((time_position or 0) * 10**6)
        self.emit_player_changes(["Position"])

    def notify(self, *args, **kwargs) -> None:
        self.on_player_all()
