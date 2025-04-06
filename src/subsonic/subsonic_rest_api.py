from dataclasses import dataclass, field
from enum import Enum

from xsdata.models.datatype import XmlDateTime

__NAMESPACE__ = "http://subsonic.org/restapi"


@dataclass(kw_only=True)
class AlbumId3:
    class Meta:
        name = "AlbumID3"

    id: str = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    name: str = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    artist: str | None = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    artist_id: str | None = field(
        default=None,
        metadata={
            "name": "artistId",
            "type": "Attribute",
        },
    )
    cover_art: str | None = field(
        default=None,
        metadata={
            "name": "coverArt",
            "type": "Attribute",
        },
    )
    song_count: int = field(
        metadata={
            "name": "songCount",
            "type": "Attribute",
            "required": True,
        }
    )
    duration: int = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    play_count: int | None = field(
        default=None,
        metadata={
            "name": "playCount",
            "type": "Attribute",
        },
    )
    created: XmlDateTime = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    starred: XmlDateTime | None = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    year: int | None = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    genre: str | None = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class AlbumInfo:
    notes: str | None = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    music_brainz_id: str | None = field(
        default=None,
        metadata={
            "name": "musicBrainzId",
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    last_fm_url: str | None = field(
        default=None,
        metadata={
            "name": "lastFmUrl",
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    small_image_url: str | None = field(
        default=None,
        metadata={
            "name": "smallImageUrl",
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    medium_image_url: str | None = field(
        default=None,
        metadata={
            "name": "mediumImageUrl",
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    large_image_url: str | None = field(
        default=None,
        metadata={
            "name": "largeImageUrl",
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )


@dataclass(kw_only=True)
class Artist:
    id: str = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    name: str = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    artist_image_url: str | None = field(
        default=None,
        metadata={
            "name": "artistImageUrl",
            "type": "Attribute",
        },
    )
    starred: XmlDateTime | None = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    user_rating: int | None = field(
        default=None,
        metadata={
            "name": "userRating",
            "type": "Attribute",
            "min_inclusive": 1,
            "max_inclusive": 5,
        },
    )
    average_rating: float | None = field(
        default=None,
        metadata={
            "name": "averageRating",
            "type": "Attribute",
            "min_inclusive": 1.0,
            "max_inclusive": 5.0,
        },
    )


@dataclass(kw_only=True)
class ArtistId3:
    class Meta:
        name = "ArtistID3"

    id: str = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    name: str = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    cover_art: str | None = field(
        default=None,
        metadata={
            "name": "coverArt",
            "type": "Attribute",
        },
    )
    artist_image_url: str | None = field(
        default=None,
        metadata={
            "name": "artistImageUrl",
            "type": "Attribute",
        },
    )
    album_count: int = field(
        metadata={
            "name": "albumCount",
            "type": "Attribute",
            "required": True,
        }
    )
    starred: XmlDateTime | None = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class ArtistInfoBase:
    biography: str | None = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    music_brainz_id: str | None = field(
        default=None,
        metadata={
            "name": "musicBrainzId",
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    last_fm_url: str | None = field(
        default=None,
        metadata={
            "name": "lastFmUrl",
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    small_image_url: str | None = field(
        default=None,
        metadata={
            "name": "smallImageUrl",
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    medium_image_url: str | None = field(
        default=None,
        metadata={
            "name": "mediumImageUrl",
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    large_image_url: str | None = field(
        default=None,
        metadata={
            "name": "largeImageUrl",
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )


@dataclass(kw_only=True)
class AudioTrack:
    id: str = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    name: str | None = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    language_code: str | None = field(
        default=None,
        metadata={
            "name": "languageCode",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Captions:
    id: str = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    name: str | None = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class ChatMessage:
    username: str = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    time: int = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    message: str = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class Error:
    code: int = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    message: str | None = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Genre:
    song_count: int = field(
        metadata={
            "name": "songCount",
            "type": "Attribute",
            "required": True,
        }
    )
    album_count: int = field(
        metadata={
            "name": "albumCount",
            "type": "Attribute",
            "required": True,
        }
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        },
    )


@dataclass(kw_only=True)
class InternetRadioStation:
    id: str = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    name: str = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    stream_url: str = field(
        metadata={
            "name": "streamUrl",
            "type": "Attribute",
            "required": True,
        }
    )
    home_page_url: str | None = field(
        default=None,
        metadata={
            "name": "homePageUrl",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class JukeboxStatus:
    current_index: int = field(
        metadata={
            "name": "currentIndex",
            "type": "Attribute",
            "required": True,
        }
    )
    playing: bool = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    gain: float = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    position: int | None = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class License:
    valid: bool = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    email: str | None = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    license_expires: XmlDateTime | None = field(
        default=None,
        metadata={
            "name": "licenseExpires",
            "type": "Attribute",
        },
    )
    trial_expires: XmlDateTime | None = field(
        default=None,
        metadata={
            "name": "trialExpires",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Lyrics:
    artist: str | None = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    title: str | None = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        },
    )


class MediaType(Enum):
    MUSIC = "music"
    PODCAST = "podcast"
    AUDIOBOOK = "audiobook"
    VIDEO = "video"


@dataclass(kw_only=True)
class MusicFolder:
    id: int = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    name: str | None = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Playlist:
    allowed_user: list[str] = field(
        default_factory=list,
        metadata={
            "name": "allowedUser",
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    id: str = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    name: str = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    comment: str | None = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    owner: str | None = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    public: bool | None = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    song_count: int = field(
        metadata={
            "name": "songCount",
            "type": "Attribute",
            "required": True,
        }
    )
    duration: int = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    created: XmlDateTime = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    changed: XmlDateTime = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    cover_art: str | None = field(
        default=None,
        metadata={
            "name": "coverArt",
            "type": "Attribute",
        },
    )


class PodcastStatus(Enum):
    NEW = "new"
    DOWNLOADING = "downloading"
    COMPLETED = "completed"
    ERROR = "error"
    DELETED = "deleted"
    SKIPPED = "skipped"


class ResponseStatus(Enum):
    OK = "ok"
    FAILED = "failed"


@dataclass(kw_only=True)
class ScanStatus:
    scanning: bool = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    count: int | None = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class User:
    folder: list[int] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    username: str = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    email: str | None = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    scrobbling_enabled: bool = field(
        metadata={
            "name": "scrobblingEnabled",
            "type": "Attribute",
            "required": True,
        }
    )
    max_bit_rate: int | None = field(
        default=None,
        metadata={
            "name": "maxBitRate",
            "type": "Attribute",
        },
    )
    admin_role: bool = field(
        metadata={
            "name": "adminRole",
            "type": "Attribute",
            "required": True,
        }
    )
    settings_role: bool = field(
        metadata={
            "name": "settingsRole",
            "type": "Attribute",
            "required": True,
        }
    )
    download_role: bool = field(
        metadata={
            "name": "downloadRole",
            "type": "Attribute",
            "required": True,
        }
    )
    upload_role: bool = field(
        metadata={
            "name": "uploadRole",
            "type": "Attribute",
            "required": True,
        }
    )
    playlist_role: bool = field(
        metadata={
            "name": "playlistRole",
            "type": "Attribute",
            "required": True,
        }
    )
    cover_art_role: bool = field(
        metadata={
            "name": "coverArtRole",
            "type": "Attribute",
            "required": True,
        }
    )
    comment_role: bool = field(
        metadata={
            "name": "commentRole",
            "type": "Attribute",
            "required": True,
        }
    )
    podcast_role: bool = field(
        metadata={
            "name": "podcastRole",
            "type": "Attribute",
            "required": True,
        }
    )
    stream_role: bool = field(
        metadata={
            "name": "streamRole",
            "type": "Attribute",
            "required": True,
        }
    )
    jukebox_role: bool = field(
        metadata={
            "name": "jukeboxRole",
            "type": "Attribute",
            "required": True,
        }
    )
    share_role: bool = field(
        metadata={
            "name": "shareRole",
            "type": "Attribute",
            "required": True,
        }
    )
    video_conversion_role: bool = field(
        metadata={
            "name": "videoConversionRole",
            "type": "Attribute",
            "required": True,
        }
    )
    avatar_last_changed: XmlDateTime | None = field(
        default=None,
        metadata={
            "name": "avatarLastChanged",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class VideoConversion:
    id: str = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    bit_rate: int | None = field(
        default=None,
        metadata={
            "name": "bitRate",
            "type": "Attribute",
        },
    )
    audio_track_id: int | None = field(
        default=None,
        metadata={
            "name": "audioTrackId",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class AlbumList2:
    album: list[AlbumId3] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )


@dataclass(kw_only=True)
class ArtistInfo(ArtistInfoBase):
    similar_artist: list[Artist] = field(
        default_factory=list,
        metadata={
            "name": "similarArtist",
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )


@dataclass(kw_only=True)
class ArtistInfo2(ArtistInfoBase):
    similar_artist: list[ArtistId3] = field(
        default_factory=list,
        metadata={
            "name": "similarArtist",
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )


@dataclass(kw_only=True)
class ArtistWithAlbumsId3(ArtistId3):
    class Meta:
        name = "ArtistWithAlbumsID3"

    album: list[AlbumId3] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )


@dataclass(kw_only=True)
class ChatMessages:
    chat_message: list[ChatMessage] = field(
        default_factory=list,
        metadata={
            "name": "chatMessage",
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )


@dataclass(kw_only=True)
class Child:
    id: str = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    parent: str | None = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    is_dir: bool = field(
        metadata={
            "name": "isDir",
            "type": "Attribute",
            "required": True,
        }
    )
    title: str = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    album: str | None = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    artist: str | None = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    track: int | None = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    year: int | None = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    genre: str | None = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    cover_art: str | None = field(
        default=None,
        metadata={
            "name": "coverArt",
            "type": "Attribute",
        },
    )
    size: int | None = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    content_type: str | None = field(
        default=None,
        metadata={
            "name": "contentType",
            "type": "Attribute",
        },
    )
    suffix: str | None = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    transcoded_content_type: str | None = field(
        default=None,
        metadata={
            "name": "transcodedContentType",
            "type": "Attribute",
        },
    )
    transcoded_suffix: str | None = field(
        default=None,
        metadata={
            "name": "transcodedSuffix",
            "type": "Attribute",
        },
    )
    duration: int | None = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    bit_rate: int | None = field(
        default=None,
        metadata={
            "name": "bitRate",
            "type": "Attribute",
        },
    )
    path: str | None = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    is_video: bool | None = field(
        default=None,
        metadata={
            "name": "isVideo",
            "type": "Attribute",
        },
    )
    user_rating: int | None = field(
        default=None,
        metadata={
            "name": "userRating",
            "type": "Attribute",
            "min_inclusive": 1,
            "max_inclusive": 5,
        },
    )
    average_rating: float | None = field(
        default=None,
        metadata={
            "name": "averageRating",
            "type": "Attribute",
            "min_inclusive": 1.0,
            "max_inclusive": 5.0,
        },
    )
    play_count: int | None = field(
        default=None,
        metadata={
            "name": "playCount",
            "type": "Attribute",
        },
    )
    disc_number: int | None = field(
        default=None,
        metadata={
            "name": "discNumber",
            "type": "Attribute",
        },
    )
    created: XmlDateTime | None = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    starred: XmlDateTime | None = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    album_id: str | None = field(
        default=None,
        metadata={
            "name": "albumId",
            "type": "Attribute",
        },
    )
    artist_id: str | None = field(
        default=None,
        metadata={
            "name": "artistId",
            "type": "Attribute",
        },
    )
    type: MediaType | None = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    bookmark_position: int | None = field(
        default=None,
        metadata={
            "name": "bookmarkPosition",
            "type": "Attribute",
        },
    )
    original_width: int | None = field(
        default=None,
        metadata={
            "name": "originalWidth",
            "type": "Attribute",
        },
    )
    original_height: int | None = field(
        default=None,
        metadata={
            "name": "originalHeight",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Genres:
    genre: list[Genre] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )


@dataclass(kw_only=True)
class Index:
    artist: list[Artist] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    name: str = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class IndexId3:
    class Meta:
        name = "IndexID3"

    artist: list[ArtistId3] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    name: str = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class InternetRadioStations:
    internet_radio_station: list[InternetRadioStation] = field(
        default_factory=list,
        metadata={
            "name": "internetRadioStation",
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )


@dataclass(kw_only=True)
class MusicFolders:
    music_folder: list[MusicFolder] = field(
        default_factory=list,
        metadata={
            "name": "musicFolder",
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )


@dataclass(kw_only=True)
class Playlists:
    playlist: list[Playlist] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )


@dataclass(kw_only=True)
class Users:
    user: list[User] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )


@dataclass(kw_only=True)
class VideoInfo:
    captions: list[Captions] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    audio_track: list[AudioTrack] = field(
        default_factory=list,
        metadata={
            "name": "audioTrack",
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    conversion: list[VideoConversion] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    id: str = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class AlbumList:
    album: list[Child] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )


@dataclass(kw_only=True)
class AlbumWithSongsId3(AlbumId3):
    class Meta:
        name = "AlbumWithSongsID3"

    song: list[Child] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )


@dataclass(kw_only=True)
class ArtistsId3:
    class Meta:
        name = "ArtistsID3"

    index: list[IndexId3] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    ignored_articles: str = field(
        metadata={
            "name": "ignoredArticles",
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class Bookmark:
    entry: Child = field(
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
            "required": True,
        }
    )
    position: int = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    username: str = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    comment: str | None = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    created: XmlDateTime = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    changed: XmlDateTime = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class Directory:
    child: list[Child] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    id: str = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    parent: str | None = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    name: str = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    starred: XmlDateTime | None = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    user_rating: int | None = field(
        default=None,
        metadata={
            "name": "userRating",
            "type": "Attribute",
            "min_inclusive": 1,
            "max_inclusive": 5,
        },
    )
    average_rating: float | None = field(
        default=None,
        metadata={
            "name": "averageRating",
            "type": "Attribute",
            "min_inclusive": 1.0,
            "max_inclusive": 5.0,
        },
    )
    play_count: int | None = field(
        default=None,
        metadata={
            "name": "playCount",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Indexes:
    shortcut: list[Artist] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    index: list[Index] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    child: list[Child] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    last_modified: int = field(
        metadata={
            "name": "lastModified",
            "type": "Attribute",
            "required": True,
        }
    )
    ignored_articles: str = field(
        metadata={
            "name": "ignoredArticles",
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class JukeboxPlaylist(JukeboxStatus):
    entry: list[Child] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )


@dataclass(kw_only=True)
class NowPlayingEntry(Child):
    username: str = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    minutes_ago: int = field(
        metadata={
            "name": "minutesAgo",
            "type": "Attribute",
            "required": True,
        }
    )
    player_id: int = field(
        metadata={
            "name": "playerId",
            "type": "Attribute",
            "required": True,
        }
    )
    player_name: str | None = field(
        default=None,
        metadata={
            "name": "playerName",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class PlayQueue:
    entry: list[Child] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    current: int | None = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    position: int | None = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    username: str = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    changed: XmlDateTime = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    changed_by: str = field(
        metadata={
            "name": "changedBy",
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class PlaylistWithSongs(Playlist):
    entry: list[Child] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )


@dataclass(kw_only=True)
class PodcastEpisode(Child):
    stream_id: str | None = field(
        default=None,
        metadata={
            "name": "streamId",
            "type": "Attribute",
        },
    )
    channel_id: str = field(
        metadata={
            "name": "channelId",
            "type": "Attribute",
            "required": True,
        }
    )
    description: str | None = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    status: PodcastStatus = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    publish_date: XmlDateTime | None = field(
        default=None,
        metadata={
            "name": "publishDate",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class SearchResult:
    match: list[Child] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    offset: int = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    total_hits: int = field(
        metadata={
            "name": "totalHits",
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class SearchResult2:
    artist: list[Artist] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    album: list[Child] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    song: list[Child] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )


@dataclass(kw_only=True)
class SearchResult3:
    artist: list[ArtistId3] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    album: list[AlbumId3] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    song: list[Child] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )


@dataclass(kw_only=True)
class Share:
    entry: list[Child] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    id: str = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    url: str = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    description: str | None = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    username: str = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    created: XmlDateTime = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    expires: XmlDateTime | None = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    last_visited: XmlDateTime | None = field(
        default=None,
        metadata={
            "name": "lastVisited",
            "type": "Attribute",
        },
    )
    visit_count: int = field(
        metadata={
            "name": "visitCount",
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass(kw_only=True)
class SimilarSongs:
    song: list[Child] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )


@dataclass(kw_only=True)
class SimilarSongs2:
    song: list[Child] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )


@dataclass(kw_only=True)
class Songs:
    song: list[Child] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )


@dataclass(kw_only=True)
class Starred:
    artist: list[Artist] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    album: list[Child] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    song: list[Child] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )


@dataclass(kw_only=True)
class Starred2:
    artist: list[ArtistId3] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    album: list[AlbumId3] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    song: list[Child] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )


@dataclass(kw_only=True)
class TopSongs:
    song: list[Child] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )


@dataclass(kw_only=True)
class Videos:
    video: list[Child] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )


@dataclass(kw_only=True)
class Bookmarks:
    bookmark: list[Bookmark] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )


@dataclass(kw_only=True)
class NewestPodcasts:
    episode: list[PodcastEpisode] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )


@dataclass(kw_only=True)
class NowPlaying:
    entry: list[NowPlayingEntry] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )


@dataclass(kw_only=True)
class PodcastChannel:
    episode: list[PodcastEpisode] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    id: str = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    url: str = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    title: str | None = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    description: str | None = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    cover_art: str | None = field(
        default=None,
        metadata={
            "name": "coverArt",
            "type": "Attribute",
        },
    )
    original_image_url: str | None = field(
        default=None,
        metadata={
            "name": "originalImageUrl",
            "type": "Attribute",
        },
    )
    status: PodcastStatus = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    error_message: str | None = field(
        default=None,
        metadata={
            "name": "errorMessage",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Shares:
    share: list[Share] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )


@dataclass(kw_only=True)
class Podcasts:
    channel: list[PodcastChannel] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )


@dataclass(kw_only=True)
class Response:
    music_folders: MusicFolders | None = field(
        default=None,
        metadata={
            "name": "musicFolders",
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    indexes: Indexes | None = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    directory: Directory | None = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    genres: Genres | None = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    artists: ArtistsId3 | None = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    artist: ArtistWithAlbumsId3 | None = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    album: AlbumWithSongsId3 | None = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    song: Child | None = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    videos: Videos | None = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    video_info: VideoInfo | None = field(
        default=None,
        metadata={
            "name": "videoInfo",
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    now_playing: NowPlaying | None = field(
        default=None,
        metadata={
            "name": "nowPlaying",
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    search_result: SearchResult | None = field(
        default=None,
        metadata={
            "name": "searchResult",
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    search_result2: SearchResult2 | None = field(
        default=None,
        metadata={
            "name": "searchResult2",
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    search_result3: SearchResult3 | None = field(
        default=None,
        metadata={
            "name": "searchResult3",
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    playlists: Playlists | None = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    playlist: PlaylistWithSongs | None = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    jukebox_status: JukeboxStatus | None = field(
        default=None,
        metadata={
            "name": "jukeboxStatus",
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    jukebox_playlist: JukeboxPlaylist | None = field(
        default=None,
        metadata={
            "name": "jukeboxPlaylist",
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    license: License | None = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    users: Users | None = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    user: User | None = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    chat_messages: ChatMessages | None = field(
        default=None,
        metadata={
            "name": "chatMessages",
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    album_list: AlbumList | None = field(
        default=None,
        metadata={
            "name": "albumList",
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    album_list2: AlbumList2 | None = field(
        default=None,
        metadata={
            "name": "albumList2",
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    random_songs: Songs | None = field(
        default=None,
        metadata={
            "name": "randomSongs",
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    songs_by_genre: Songs | None = field(
        default=None,
        metadata={
            "name": "songsByGenre",
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    lyrics: Lyrics | None = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    podcasts: Podcasts | None = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    newest_podcasts: NewestPodcasts | None = field(
        default=None,
        metadata={
            "name": "newestPodcasts",
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    internet_radio_stations: InternetRadioStations | None = field(
        default=None,
        metadata={
            "name": "internetRadioStations",
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    bookmarks: Bookmarks | None = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    play_queue: PlayQueue | None = field(
        default=None,
        metadata={
            "name": "playQueue",
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    shares: Shares | None = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    starred: Starred | None = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    starred2: Starred2 | None = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    album_info: AlbumInfo | None = field(
        default=None,
        metadata={
            "name": "albumInfo",
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    artist_info: ArtistInfo | None = field(
        default=None,
        metadata={
            "name": "artistInfo",
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    artist_info2: ArtistInfo2 | None = field(
        default=None,
        metadata={
            "name": "artistInfo2",
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    similar_songs: SimilarSongs | None = field(
        default=None,
        metadata={
            "name": "similarSongs",
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    similar_songs2: SimilarSongs2 | None = field(
        default=None,
        metadata={
            "name": "similarSongs2",
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    top_songs: TopSongs | None = field(
        default=None,
        metadata={
            "name": "topSongs",
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    scan_status: ScanStatus | None = field(
        default=None,
        metadata={
            "name": "scanStatus",
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    error: Error | None = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    status: ResponseStatus = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    version: str = field(
        metadata={
            "type": "Attribute",
            "required": True,
            "pattern": r"\d+\.\d+\.\d+",
        }
    )


@dataclass(kw_only=True)
class SubsonicResponse(Response):
    class Meta:
        name = "subsonic-response"
        namespace = "http://subsonic.org/restapi"
