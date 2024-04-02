from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional

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
    artist: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    artist_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "artistId",
            "type": "Attribute",
        },
    )
    cover_art: Optional[str] = field(
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
    play_count: Optional[int] = field(
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
    starred: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    year: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    genre: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class AlbumInfo:
    notes: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    music_brainz_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "musicBrainzId",
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    last_fm_url: Optional[str] = field(
        default=None,
        metadata={
            "name": "lastFmUrl",
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    small_image_url: Optional[str] = field(
        default=None,
        metadata={
            "name": "smallImageUrl",
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    medium_image_url: Optional[str] = field(
        default=None,
        metadata={
            "name": "mediumImageUrl",
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    large_image_url: Optional[str] = field(
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
    artist_image_url: Optional[str] = field(
        default=None,
        metadata={
            "name": "artistImageUrl",
            "type": "Attribute",
        },
    )
    starred: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    user_rating: Optional[int] = field(
        default=None,
        metadata={
            "name": "userRating",
            "type": "Attribute",
            "min_inclusive": 1,
            "max_inclusive": 5,
        },
    )
    average_rating: Optional[float] = field(
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
    cover_art: Optional[str] = field(
        default=None,
        metadata={
            "name": "coverArt",
            "type": "Attribute",
        },
    )
    artist_image_url: Optional[str] = field(
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
    starred: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class ArtistInfoBase:
    biography: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    music_brainz_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "musicBrainzId",
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    last_fm_url: Optional[str] = field(
        default=None,
        metadata={
            "name": "lastFmUrl",
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    small_image_url: Optional[str] = field(
        default=None,
        metadata={
            "name": "smallImageUrl",
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    medium_image_url: Optional[str] = field(
        default=None,
        metadata={
            "name": "mediumImageUrl",
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    large_image_url: Optional[str] = field(
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
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    language_code: Optional[str] = field(
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
    name: Optional[str] = field(
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
    message: Optional[str] = field(
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
    content: List[object] = field(
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
    home_page_url: Optional[str] = field(
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
    position: Optional[int] = field(
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
    email: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    license_expires: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "licenseExpires",
            "type": "Attribute",
        },
    )
    trial_expires: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "trialExpires",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Lyrics:
    artist: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    content: List[object] = field(
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
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Playlist:
    allowed_user: List[str] = field(
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
    comment: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    owner: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    public: Optional[bool] = field(
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
    cover_art: Optional[str] = field(
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
    count: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class User:
    folder: List[int] = field(
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
    email: Optional[str] = field(
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
    max_bit_rate: Optional[int] = field(
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
    avatar_last_changed: Optional[XmlDateTime] = field(
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
    bit_rate: Optional[int] = field(
        default=None,
        metadata={
            "name": "bitRate",
            "type": "Attribute",
        },
    )
    audio_track_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "audioTrackId",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class AlbumList2:
    album: List[AlbumId3] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )


@dataclass(kw_only=True)
class ArtistInfo(ArtistInfoBase):
    similar_artist: List[Artist] = field(
        default_factory=list,
        metadata={
            "name": "similarArtist",
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )


@dataclass(kw_only=True)
class ArtistInfo2(ArtistInfoBase):
    similar_artist: List[ArtistId3] = field(
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

    album: List[AlbumId3] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )


@dataclass(kw_only=True)
class ChatMessages:
    chat_message: List[ChatMessage] = field(
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
    parent: Optional[str] = field(
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
    album: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    artist: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    track: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    year: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    genre: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    cover_art: Optional[str] = field(
        default=None,
        metadata={
            "name": "coverArt",
            "type": "Attribute",
        },
    )
    size: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "contentType",
            "type": "Attribute",
        },
    )
    suffix: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    transcoded_content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "transcodedContentType",
            "type": "Attribute",
        },
    )
    transcoded_suffix: Optional[str] = field(
        default=None,
        metadata={
            "name": "transcodedSuffix",
            "type": "Attribute",
        },
    )
    duration: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    bit_rate: Optional[int] = field(
        default=None,
        metadata={
            "name": "bitRate",
            "type": "Attribute",
        },
    )
    path: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    is_video: Optional[bool] = field(
        default=None,
        metadata={
            "name": "isVideo",
            "type": "Attribute",
        },
    )
    user_rating: Optional[int] = field(
        default=None,
        metadata={
            "name": "userRating",
            "type": "Attribute",
            "min_inclusive": 1,
            "max_inclusive": 5,
        },
    )
    average_rating: Optional[float] = field(
        default=None,
        metadata={
            "name": "averageRating",
            "type": "Attribute",
            "min_inclusive": 1.0,
            "max_inclusive": 5.0,
        },
    )
    play_count: Optional[int] = field(
        default=None,
        metadata={
            "name": "playCount",
            "type": "Attribute",
        },
    )
    disc_number: Optional[int] = field(
        default=None,
        metadata={
            "name": "discNumber",
            "type": "Attribute",
        },
    )
    created: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    starred: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    album_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "albumId",
            "type": "Attribute",
        },
    )
    artist_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "artistId",
            "type": "Attribute",
        },
    )
    type: Optional[MediaType] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    bookmark_position: Optional[int] = field(
        default=None,
        metadata={
            "name": "bookmarkPosition",
            "type": "Attribute",
        },
    )
    original_width: Optional[int] = field(
        default=None,
        metadata={
            "name": "originalWidth",
            "type": "Attribute",
        },
    )
    original_height: Optional[int] = field(
        default=None,
        metadata={
            "name": "originalHeight",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Genres:
    genre: List[Genre] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )


@dataclass(kw_only=True)
class Index:
    artist: List[Artist] = field(
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

    artist: List[ArtistId3] = field(
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
    internet_radio_station: List[InternetRadioStation] = field(
        default_factory=list,
        metadata={
            "name": "internetRadioStation",
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )


@dataclass(kw_only=True)
class MusicFolders:
    music_folder: List[MusicFolder] = field(
        default_factory=list,
        metadata={
            "name": "musicFolder",
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )


@dataclass(kw_only=True)
class Playlists:
    playlist: List[Playlist] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )


@dataclass(kw_only=True)
class Users:
    user: List[User] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )


@dataclass(kw_only=True)
class VideoInfo:
    captions: List[Captions] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    audio_track: List[AudioTrack] = field(
        default_factory=list,
        metadata={
            "name": "audioTrack",
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    conversion: List[VideoConversion] = field(
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
    album: List[Child] = field(
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

    song: List[Child] = field(
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

    index: List[IndexId3] = field(
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
    comment: Optional[str] = field(
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
    child: List[Child] = field(
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
    parent: Optional[str] = field(
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
    starred: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    user_rating: Optional[int] = field(
        default=None,
        metadata={
            "name": "userRating",
            "type": "Attribute",
            "min_inclusive": 1,
            "max_inclusive": 5,
        },
    )
    average_rating: Optional[float] = field(
        default=None,
        metadata={
            "name": "averageRating",
            "type": "Attribute",
            "min_inclusive": 1.0,
            "max_inclusive": 5.0,
        },
    )
    play_count: Optional[int] = field(
        default=None,
        metadata={
            "name": "playCount",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Indexes:
    shortcut: List[Artist] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    index: List[Index] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    child: List[Child] = field(
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
    entry: List[Child] = field(
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
    player_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "playerName",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class PlayQueue:
    entry: List[Child] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    current: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    position: Optional[int] = field(
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
    entry: List[Child] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )


@dataclass(kw_only=True)
class PodcastEpisode(Child):
    stream_id: Optional[str] = field(
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
    description: Optional[str] = field(
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
    publish_date: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "publishDate",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class SearchResult:
    match: List[Child] = field(
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
    artist: List[Artist] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    album: List[Child] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    song: List[Child] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )


@dataclass(kw_only=True)
class SearchResult3:
    artist: List[ArtistId3] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    album: List[AlbumId3] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    song: List[Child] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )


@dataclass(kw_only=True)
class Share:
    entry: List[Child] = field(
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
    description: Optional[str] = field(
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
    expires: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    last_visited: Optional[XmlDateTime] = field(
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
    song: List[Child] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )


@dataclass(kw_only=True)
class SimilarSongs2:
    song: List[Child] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )


@dataclass(kw_only=True)
class Songs:
    song: List[Child] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )


@dataclass(kw_only=True)
class Starred:
    artist: List[Artist] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    album: List[Child] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    song: List[Child] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )


@dataclass(kw_only=True)
class Starred2:
    artist: List[ArtistId3] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    album: List[AlbumId3] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    song: List[Child] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )


@dataclass(kw_only=True)
class TopSongs:
    song: List[Child] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )


@dataclass(kw_only=True)
class Videos:
    video: List[Child] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )


@dataclass(kw_only=True)
class Bookmarks:
    bookmark: List[Bookmark] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )


@dataclass(kw_only=True)
class NewestPodcasts:
    episode: List[PodcastEpisode] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )


@dataclass(kw_only=True)
class NowPlaying:
    entry: List[NowPlayingEntry] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )


@dataclass(kw_only=True)
class PodcastChannel:
    episode: List[PodcastEpisode] = field(
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
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    description: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    cover_art: Optional[str] = field(
        default=None,
        metadata={
            "name": "coverArt",
            "type": "Attribute",
        },
    )
    original_image_url: Optional[str] = field(
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
    error_message: Optional[str] = field(
        default=None,
        metadata={
            "name": "errorMessage",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Shares:
    share: List[Share] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )


@dataclass(kw_only=True)
class Podcasts:
    channel: List[PodcastChannel] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )


@dataclass(kw_only=True)
class Response:
    music_folders: Optional[MusicFolders] = field(
        default=None,
        metadata={
            "name": "musicFolders",
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    indexes: Optional[Indexes] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    directory: Optional[Directory] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    genres: Optional[Genres] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    artists: Optional[ArtistsId3] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    artist: Optional[ArtistWithAlbumsId3] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    album: Optional[AlbumWithSongsId3] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    song: Optional[Child] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    videos: Optional[Videos] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    video_info: Optional[VideoInfo] = field(
        default=None,
        metadata={
            "name": "videoInfo",
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    now_playing: Optional[NowPlaying] = field(
        default=None,
        metadata={
            "name": "nowPlaying",
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    search_result: Optional[SearchResult] = field(
        default=None,
        metadata={
            "name": "searchResult",
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    search_result2: Optional[SearchResult2] = field(
        default=None,
        metadata={
            "name": "searchResult2",
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    search_result3: Optional[SearchResult3] = field(
        default=None,
        metadata={
            "name": "searchResult3",
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    playlists: Optional[Playlists] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    playlist: Optional[PlaylistWithSongs] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    jukebox_status: Optional[JukeboxStatus] = field(
        default=None,
        metadata={
            "name": "jukeboxStatus",
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    jukebox_playlist: Optional[JukeboxPlaylist] = field(
        default=None,
        metadata={
            "name": "jukeboxPlaylist",
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    license: Optional[License] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    users: Optional[Users] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    user: Optional[User] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    chat_messages: Optional[ChatMessages] = field(
        default=None,
        metadata={
            "name": "chatMessages",
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    album_list: Optional[AlbumList] = field(
        default=None,
        metadata={
            "name": "albumList",
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    album_list2: Optional[AlbumList2] = field(
        default=None,
        metadata={
            "name": "albumList2",
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    random_songs: Optional[Songs] = field(
        default=None,
        metadata={
            "name": "randomSongs",
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    songs_by_genre: Optional[Songs] = field(
        default=None,
        metadata={
            "name": "songsByGenre",
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    lyrics: Optional[Lyrics] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    podcasts: Optional[Podcasts] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    newest_podcasts: Optional[NewestPodcasts] = field(
        default=None,
        metadata={
            "name": "newestPodcasts",
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    internet_radio_stations: Optional[InternetRadioStations] = field(
        default=None,
        metadata={
            "name": "internetRadioStations",
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    bookmarks: Optional[Bookmarks] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    play_queue: Optional[PlayQueue] = field(
        default=None,
        metadata={
            "name": "playQueue",
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    shares: Optional[Shares] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    starred: Optional[Starred] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    starred2: Optional[Starred2] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    album_info: Optional[AlbumInfo] = field(
        default=None,
        metadata={
            "name": "albumInfo",
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    artist_info: Optional[ArtistInfo] = field(
        default=None,
        metadata={
            "name": "artistInfo",
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    artist_info2: Optional[ArtistInfo2] = field(
        default=None,
        metadata={
            "name": "artistInfo2",
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    similar_songs: Optional[SimilarSongs] = field(
        default=None,
        metadata={
            "name": "similarSongs",
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    similar_songs2: Optional[SimilarSongs2] = field(
        default=None,
        metadata={
            "name": "similarSongs2",
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    top_songs: Optional[TopSongs] = field(
        default=None,
        metadata={
            "name": "topSongs",
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    scan_status: Optional[ScanStatus] = field(
        default=None,
        metadata={
            "name": "scanStatus",
            "type": "Element",
            "namespace": "http://subsonic.org/restapi",
        },
    )
    error: Optional[Error] = field(
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
