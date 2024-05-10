from textual.app import ComposeResult
from textual.containers import Container
from textual.message import Message
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Tree
from typing_extensions import override

from rorqual.media_library import MediaLibrary
from rorqual.subsonic_client import SubsonicClient
from subsonic.subsonic_rest_api import AlbumId3, AlbumWithSongsId3, ArtistId3


class AlbumTree(Widget):
    class AddAlbumToPlaylist(Message):
        def __init__(self, album: AlbumWithSongsId3) -> None:
            super().__init__()
            self.album = album

    media_library = reactive[MediaLibrary | None](None)

    BINDINGS = [
        ("j", "down", "Down"),
        ("k", "up", "Up"),
        ("l", "expand", "Expand"),
        ("h", "collapse", "Collapse"),
        ("a", "add_to_playlist", "Add to playlist"),
    ]

    DEFAULT_CSS = """
    AlbumTree Tree {
        background: $background;
    }

    AlbumTree Tree > .tree--guides {
        color: $surface;
    }

    AlbumTree Tree > .tree--guides-hover {
        color: $warning;
        text-style: bold;
    }

    AlbumTree Tree > .tree--guides-selected {
        color: $warning;
        text-style: bold;
    }
    """

    def __init__(self, subsonic: SubsonicClient) -> None:
        super().__init__()
        self.subsonic = subsonic

    @override
    def compose(self) -> ComposeResult:
        yield Container(id="tree")

    def watch_media_library(self, media_library: MediaLibrary | None):
        if media_library is None:
            return

        artists_tree = Tree[ArtistId3 | AlbumId3]("Artists")
        artists_tree.guide_depth = 2
        artists_tree.root.expand()

        for artist in media_library.artists.values():
            artists_tree.root.add(artist.name, data=artist, expand=False)

        for node in artists_tree.root.children:
            assert node.data is not None
            for album in media_library.albums_by_artist.get(node.data.id, []):
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
