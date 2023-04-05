from itertools import groupby

from textual.app import App, ComposeResult
from textual.containers import Container, Vertical
from textual.message import Message
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import DataTable, Tree

from rorqual.subsonic_client import SubsonicClient
from rorqual.subsonic_player import SubsonicPlayer
from subsonic.subsonic_rest_api import AlbumId3, AlbumWithSongsId3, ArtistId3


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

    def __init__(self, subsonic: SubsonicClient, id: str) -> None:
        super().__init__(id=id)
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


class Playlist(Widget):
    tracks = reactive(list[tuple[str, int | None, str]]())

    def compose(self) -> ComposeResult:
        table = DataTable()
        table.add_columns("#", "Title")
        yield table

    def watch_tracks(self, new_tracks: list[tuple[str, int | None, str]]) -> None:
        table = self.query_one(DataTable)
        assert table is not None
        table.clear()

        for id, track_number, title in new_tracks:
            table.add_row(track_number, title)


class RorqualApp(App):
    BINDINGS = [("q", "quit", "Quit")]

    DEFAULT_CSS = """
    #album-tree {
        dock: left;
        width: 25%;
        height: 100%;
    }

    #playlist {
        height: 100%;
    }
    """

    def __init__(self, subsonic: SubsonicClient, player: SubsonicPlayer) -> None:
        super().__init__()
        self.subsonic = subsonic
        self.player = player

    def compose(self) -> ComposeResult:
        yield AlbumTree(self.subsonic, id="album-tree")
        with Vertical():
            yield Playlist(id="playlist")

    def on_album_tree_add_album_to_playlist(self, message: AlbumTree.AddAlbumToPlaylist) -> None:
        playlist = self.query_one(Playlist)
        assert playlist is not None
        playlist.tracks = [(song.id, song.track, song.title) for song in message.album.song]
