from contextlib import suppress
from datetime import timedelta
from typing import override

from textual import events, on, work
from textual.app import App, ComposeResult
from textual.containers import Vertical

from subsonic.subsonic_rest_api import Child

from .media_library import MediaLibrary
from .stream_manager import StreamManager
from .subsonic_client import NotCached, SubsonicClient
from .subsonic_player import PlaybackState, SubsonicPlayer
from .ui.album_tree import AlbumTree
from .ui.playback_progress import PlaybackProgress
from .ui.playlist import Playlist

LIBRARY_REFRESH_INTERVAL = timedelta(minutes=10)


class RorqualApp(App[None]):
    BINDINGS = [("q", "quit", "Quit")]

    DEFAULT_CSS = """
    AlbumTree {
        dock: left;
        width: 25%;
        min-width: 40;
        height: 100%;
    }

    Playlist {
        height: 100%;
    }

    PlaybackProgress {
        dock: bottom;
        text-align: right;
        height: 1;
    }
    """

    def __init__(
        self,
        subsonic: SubsonicClient,
        player: SubsonicPlayer,
        stream_manager: StreamManager,
    ) -> None:
        super().__init__()
        self.subsonic = subsonic
        self.player = player
        self.stream_manager = stream_manager

    @override
    def compose(self) -> ComposeResult:
        yield AlbumTree(self.subsonic, self.stream_manager)
        with Vertical():
            yield Playlist(self.stream_manager)
            yield PlaybackProgress()

    @property
    def playlist(self) -> Playlist:
        return self.query_one(Playlist)

    @property
    def album_tree(self) -> AlbumTree:
        return self.query_one(AlbumTree)

    @property
    def playback_progress(self) -> PlaybackProgress:
        return self.query_one(PlaybackProgress)

    @on(events.Mount)
    async def initialize(self) -> None:
        self.theme = "nord"

        self.player.time_position_callbacks.register(self.handle_time_pos_updated)
        self.player.playlist_content_callbacks.register(self.handle_playlist_content_change)
        self.player.playback_state_callbacks.register(self.handle_playback_state_change)
        self.player.playlist_position_callbacks.register(self.handle_playlist_track_changed)

        # Stale-while-revalidate: show whatever we have right away, then refresh it periodically
        with suppress(NotCached):
            self.album_tree.media_library = await MediaLibrary.fetch(self.subsonic, cache_only=True)

        self.refresh_media_library()
        self.set_interval(LIBRARY_REFRESH_INTERVAL.total_seconds(), self.refresh_media_library)

    @work(exclusive=True)
    async def refresh_media_library(self) -> None:
        try:
            self.album_tree.media_library = await MediaLibrary.fetch(self.subsonic)
        except NotCached as error:
            self.notify(f"Could not load the media library: {error}", severity="error")

    @on(AlbumTree.AddAlbumToPlaylist)
    def add_album_to_playlist(self, message: AlbumTree.AddAlbumToPlaylist) -> None:
        self.playlist.albums[message.album.id] = message.album
        self.player.playlist_append(message.album.song)

    @on(Playlist.TrackSelected)
    def select_track(self, message: Playlist.TrackSelected) -> None:
        if message.track_index != self.playlist.track_index:
            self.player.play(message.track_index)
        else:
            self.player.toggle_paused()

    @on(Playlist.PlayPause)
    def play_pause(self) -> None:
        self.player.toggle_paused()

    @on(Playlist.ClearPlaylist)
    def clear_playlist(self) -> None:
        self.player.playlist_clear()

    def handle_playlist_content_change(self, playlist: list[Child]) -> None:
        self.playlist.tracks = playlist

    def handle_playlist_track_changed(self, track_index: int | None) -> None:
        self.playlist.track_index = track_index

        if track_index is not None:
            self.playback_progress.track = self.playlist.tracks[track_index]

    def handle_time_pos_updated(self, time_pos: float | None) -> None:
        self.playback_progress.position = int(time_pos or 0.0)

    def handle_playback_state_change(self, state: PlaybackState) -> None:
        self.playlist.playback_state = state
        self.playback_progress.playback_state = state
