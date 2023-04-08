from itertools import groupby

from rich.console import RenderableType
from rich.emoji import Emoji
from textual.app import App, ComposeResult
from textual.containers import Container, Vertical
from textual.coordinate import Coordinate
from textual.message import Message
from textual.reactive import reactive, var
from textual.widget import Widget
from textual.widgets import DataTable, Tree

from rorqual.subsonic_client import SubsonicClient
from rorqual.subsonic_player import PlaybackState, SubsonicPlayer
from subsonic.subsonic_rest_api import AlbumId3, AlbumWithSongsId3, ArtistId3, Child


class AlbumTree(Widget):
    class AddAlbumToPlaylist(Message):
        def __init__(self, album: AlbumWithSongsId3) -> None:
            super().__init__()
            self.album = album

    BINDINGS = [
        ("j", "down", "Down"),
        ("k", "up", "Up"),
        ("l", "expand", "Expand"),
        ("h", "collapse", "Collapse"),
        ("a", "add_to_playlist", "Add to playlist"),
    ]

    def __init__(self, subsonic: SubsonicClient) -> None:
        super().__init__()
        self.subsonic = subsonic

    def compose(self) -> ComposeResult:
        yield Container(id="tree")

    async def on_mount(self):
        artists = await self.subsonic.get_artists()
        albums = {
            str(artist_id): sorted(albums, key=lambda album: album.year or 0)
            for artist_id, albums in groupby(await self.subsonic.get_albums(), key=lambda album: album.artist_id or "")
        }

        artists_tree = Tree[ArtistId3 | AlbumId3]("Artists")
        artists_tree.guide_depth = 2
        artists_tree.root.expand()

        for artist in artists:
            artists_tree.root.add(artist.name, data=artist, expand=False)

        for node in artists_tree.root.children:
            assert node.data is not None
            for album in albums.get(node.data.id, []):
                node.add(f"[{album.year}] {album.name}", data=album)

        self.query_one(Container).mount(artists_tree)
        artists_tree.focus()

    def action_down(self) -> None:
        self.query_one(Tree).action_cursor_down()

    def action_up(self) -> None:
        self.query_one(Tree).action_cursor_up()

    def action_expand(self) -> None:
        tree = self.query_one(Tree)
        if tree.cursor_node:
            tree.cursor_node.expand()

    def action_collapse(self) -> None:
        tree = self.query_one(Tree)
        if tree.cursor_node:
            tree.cursor_node.collapse()

    async def action_add_to_playlist(self) -> None:
        node = self.query_one(Tree).cursor_node

        if node and isinstance(node.data, AlbumId3):
            album = await self.subsonic.get_album_details(node.data.id)
            self.post_message(self.AddAlbumToPlaylist(album))


def duration(seconds: int) -> str:
    minutes, seconds = divmod(seconds, 60)
    return f"{minutes}:{seconds:02}"


class Playlist(Widget):
    tracks = reactive(list[Child]())
    track_index = reactive[int | None](None)
    playback_state = reactive[PlaybackState]("stopped")
    highlighted_row = var[int](0)

    @property
    def current_track(self) -> Child | None:
        if self.track_index is None or self.track_index not in range(0, len(self.tracks)):
            return None

        return self.tracks[self.track_index]

    @property
    def next_track(self) -> Child | None:
        if self.track_index is None or self.track_index + 1 >= len(self.tracks):
            return None

        return self.tracks[self.track_index + 1]

    BINDINGS = [
        ("j", "down", "Down"),
        ("k", "up", "Up"),
        ("space", "toggle", "Play/Pause"),
    ]

    class TrackSelected(Message):
        def __init__(self, track_index: int, track: Child) -> None:
            super().__init__()
            self.track_index = track_index
            self.track = track

    class PlayPause(Message):
        pass

    def compose(self) -> ComposeResult:
        table = DataTable()
        table.cursor_type = "row"
        table.add_column("", width=1)
        table.add_column("#", width=3)
        table.add_column("Title")
        table.add_column("Time", width=5)
        yield table

    def watch_tracks(self, new_tracks: list[Child]) -> None:
        self._fill_table()

    def watch_track_index(self, new_track_index: int | None) -> None:
        self._fill_table()

    def watch_playback_state(self, new_state: PlaybackState) -> None:
        self._fill_table()

    def _fill_table(self) -> None:
        table = self.query_one(DataTable)
        table.clear()

        if self.playback_state == "playing":
            icon = Emoji("play_button")
        elif self.playback_state == "paused":
            icon = Emoji("pause_button")
        else:
            icon = None

        for index, track in enumerate(self.tracks):
            table.add_row(
                icon if index == self.track_index else None,
                track.track,
                track.title,
                duration(track.duration or 0),
                key=track.id,
            )

        table.cursor_coordinate = Coordinate(min(len(self.tracks), self.highlighted_row), 0)

    def on_data_table_row_selected(self, message: DataTable.RowSelected) -> None:
        for track in self.tracks:
            if track.id == message.row_key.value:
                self.post_message(self.TrackSelected(message.cursor_row, track))
                return

    def on_data_table_row_highlighted(self, message: DataTable.RowHighlighted) -> None:
        self.highlighted_row = message.cursor_row

    def action_down(self) -> None:
        self.query_one(DataTable).action_cursor_down()

    def action_up(self) -> None:
        self.query_one(DataTable).action_cursor_up()

    def action_toggle(self) -> None:
        self.post_message(self.PlayPause())


class PlaybackProgress(Widget):
    track = reactive[Child | None](None)
    position = reactive[int](0)
    playback_state = reactive[PlaybackState]("stopped")

    def render(self) -> RenderableType:
        if self.track is None or self.playback_state == "stopped":
            return "Not playing"

        status = "Playing" if self.playback_state == "playing" else "Paused"

        return f"{status} {duration(self.position)} / {duration(self.track.duration or 0)}"


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

    def __init__(self, subsonic: SubsonicClient, player: SubsonicPlayer) -> None:
        super().__init__()
        self.subsonic = subsonic
        self.player = player

    def compose(self) -> ComposeResult:
        yield AlbumTree(self.subsonic)
        with Vertical():
            yield Playlist()
            yield PlaybackProgress()

    @property
    def playlist(self) -> Playlist:
        return self.query_one(Playlist)

    @property
    def playback_progress(self) -> PlaybackProgress:
        return self.query_one(PlaybackProgress)

    def on_mount(self) -> None:
        self.player.time_position_callbacks.register(self.on_time_pos_updated)
        self.player.next_track_start_callbacks.register(self.on_next_track_start)
        self.player.playback_state_callbacks.register(self.on_playback_state_change)

    def on_album_tree_add_album_to_playlist(self, message: AlbumTree.AddAlbumToPlaylist) -> None:
        self.playlist.tracks = message.album.song

    def on_playlist_track_selected(self, message: Playlist.TrackSelected) -> None:
        self.playback_progress.track = message.track
        self.playlist.track_index = message.track_index

        if message.track.id != self.player.playing_track:
            self.player.play(message.track.id)
            if next_track := self.playlist.next_track:
                self.player.set_next_track(next_track.id)
        else:
            self.player.toggle_paused()

    def on_playlist_play_pause(self) -> None:
        self.player.toggle_paused()

    def on_time_pos_updated(self, time_pos: float | None) -> None:
        self.playback_progress.position = int(time_pos or 0.0)

    def on_next_track_start(self) -> None:
        if self.playlist.track_index is None:
            raise RuntimeError("Inconsistent state")

        self.playlist.track_index += 1
        self.playback_progress.track = self.playlist.current_track

        if next_track := self.playlist.next_track:
            self.player.set_next_track(next_track.id)

    def on_playback_state_change(self, state: PlaybackState) -> None:
        self.playlist.playback_state = state
        self.playback_progress.playback_state = state
