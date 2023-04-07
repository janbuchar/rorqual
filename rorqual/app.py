from itertools import groupby

from rich.console import RenderableType
from textual.app import App, ComposeResult
from textual.containers import Container, Vertical
from textual.message import Message
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import DataTable, Tree

from rorqual.subsonic_client import SubsonicClient
from rorqual.subsonic_player import SubsonicPlayer
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

    BINDINGS = [
        ("j", "down", "Down"),
        ("k", "up", "Up"),
    ]

    class TrackSelected(Message):
        def __init__(self, track: Child) -> None:
            super().__init__()
            self.track = track

    def compose(self) -> ComposeResult:
        table = DataTable()
        table.cursor_type = "row"
        table.add_column("#", width=3)
        table.add_column("Title")
        table.add_column("Time", width=5)
        yield table

    def watch_tracks(self, new_tracks: list[Child]) -> None:
        table = self.query_one(DataTable)
        assert table is not None
        table.clear()

        for track in new_tracks:
            table.add_row(track.track, track.title, duration(track.duration or 0), key=track.id)

    def on_data_table_row_selected(self, message: DataTable.RowSelected) -> None:
        for track in self.tracks:
            if track.id == message.row_key.value:
                self.post_message(self.TrackSelected(track))
                return

    def action_down(self) -> None:
        self.query_one(DataTable).action_cursor_down()

    def action_up(self) -> None:
        self.query_one(DataTable).action_cursor_up()


class PlaybackProgress(Widget):
    track = reactive[Child | None](None)
    position = reactive[int](0)

    def render(self) -> RenderableType:
        if self.track is None:
            return "Not playing"

        return f"{duration(self.position)} / {duration(self.track.duration or 0)}"


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

    def on_mount(self) -> None:
        self.player.register_time_position_callback(self.on_time_pos_updated)

    def on_album_tree_add_album_to_playlist(self, message: AlbumTree.AddAlbumToPlaylist) -> None:
        playlist = self.query_one(Playlist)
        playlist.tracks = message.album.song

    def on_playlist_track_selected(self, message: Playlist.TrackSelected) -> None:
        playback_progress = self.query_one(PlaybackProgress)
        playback_progress.track = message.track

        if message.track.id != self.player.playing_track:
            self.player.play(message.track.id)
        else:
            self.player.toggle_paused()

    def on_time_pos_updated(self, time_pos: float | None) -> None:
        playback_progress = self.query_one(PlaybackProgress)
        playback_progress.position = int(time_pos or 0.0)
