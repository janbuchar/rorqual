from textual.app import App, ComposeResult
from textual.containers import Vertical

from subsonic.subsonic_rest_api import Child

from .media_library import MediaLibrary
from .stream_manager import StreamManager
from .subsonic_client import SubsonicClient
from .subsonic_player import PlaybackState, SubsonicPlayer
from .ui.album_tree import AlbumTree
from .ui.playback_progress import PlaybackProgress
from .ui.playlist import Playlist


class RorqualApp(App):
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

    def __init__(self, subsonic: SubsonicClient, player: SubsonicPlayer, stream_manager: StreamManager) -> None:
        super().__init__()
        self.subsonic = subsonic
        self.player = player
        self.stream_manager = stream_manager

    def compose(self) -> ComposeResult:
        yield AlbumTree(self.subsonic)
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

    async def on_mount(self) -> None:
        self.player.time_position_callbacks.register(self.on_time_pos_updated)
        self.player.playlist_content_callbacks.register(self.on_playlist_content_change)
        self.player.playback_state_callbacks.register(self.on_playback_state_change)
        self.player.playlist_position_callbacks.register(self.on_playlist_track_changed)

        media_library = await MediaLibrary.fetch(self.subsonic)
        self.playlist.media_library = media_library
        self.album_tree.media_library = media_library

    def on_album_tree_add_album_to_playlist(self, message: AlbumTree.AddAlbumToPlaylist) -> None:
        self.player.playlist_append(message.album.song)

    def on_playlist_content_change(self, playlist: list[Child]) -> None:
        self.playlist.tracks = playlist

    def on_playlist_track_changed(self, track_index: int | None) -> None:
        self.playlist.track_index = track_index

        if track_index is not None:
            self.playback_progress.track = self.playlist.tracks[track_index]

    def on_playlist_track_selected(self, message: Playlist.TrackSelected) -> None:
        if message.track_index != self.playlist.track_index:
            self.player.play(message.track_index)
        else:
            self.player.toggle_paused()

    def on_playlist_play_pause(self) -> None:
        self.player.toggle_paused()

    def on_time_pos_updated(self, time_pos: float | None) -> None:
        self.playback_progress.position = int(time_pos or 0.0)

    def on_playback_state_change(self, state: PlaybackState) -> None:
        self.playlist.playback_state = state
        self.playback_progress.playback_state = state

    def on_playlist_clear_playlist(self) -> None:
        self.player.playlist_clear()
