from dataclasses import dataclass
from typing import List, Optional

__all__ = ["SongMetadata"]


@dataclass
class SongMetadata:
    title: str
    artist: str
    artists: List[str]
    album_name: Optional[str]
    album_artist: Optional[str]
    track_number: int
    track_count: int
    disc_number: int
    disc_count: int
    genres: List[str]
    date: str
    year: int
    explicit: bool
    cover_url: Optional[str]
    lyrics: Optional[str]
    download_url: Optional[str]
    url: Optional[str]
    publisher: Optional[str]
    popularity: Optional[int]
    copyright_text: Optional[str]
