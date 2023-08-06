from .song_metadata import SongMetadata
from .tag_preset import TagPreset
from .embed_metadata_command import EmbedMetadataCommand
from .embedders import (
    FlacMetadataEmbedder,
    M4AMetadataEmbedder,
    Mp3MetadataEmbedder,
    OggMetadataEmbedder,
    OpusMetadataEmbedder,
)
from .handlers import (
    FlacMetadataHandler,
    M4AMetadataHandler,
    Mp3MetadataHandler,
    OggMetadataHandler,
    OpusMetadataHandler,
)

__all__ = [
    "SongMetadata",
    "TagPreset",
    "EmbedMetadataCommand",
    "FlacMetadataEmbedder",
    "M4AMetadataEmbedder",
    "Mp3MetadataEmbedder",
    "OggMetadataEmbedder",
    "OpusMetadataEmbedder",
    "FlacMetadataHandler",
    "M4AMetadataHandler",
    "Mp3MetadataHandler",
    "OggMetadataHandler",
    "OpusMetadataHandler",
]
