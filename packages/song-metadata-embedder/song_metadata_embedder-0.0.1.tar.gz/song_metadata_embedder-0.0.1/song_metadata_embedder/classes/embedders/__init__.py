from .abstract_metadata_embedder import AbstractMetadataEmbedder

from .flac_metadata_embedder import FlacMetadataEmbedder
from .m4a_metadata_embedder import M4AMetadataEmbedder
from .mp3_metadata_embedder import Mp3MetadataEmbedder
from .ogg_metadata_embedder import OggMetadataEmbedder
from .opus_metadata_embedder import OpusMetadataEmbedder

__all__ = [
    "AbstractMetadataEmbedder",
    "FlacMetadataEmbedder",
    "M4AMetadataEmbedder",
    "Mp3MetadataEmbedder",
    "OggMetadataEmbedder",
    "OpusMetadataEmbedder",
]
