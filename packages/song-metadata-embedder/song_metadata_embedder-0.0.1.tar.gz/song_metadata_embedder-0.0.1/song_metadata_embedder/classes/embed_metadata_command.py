from dataclasses import dataclass
from pathlib import Path

from song_metadata_embedder.classes import SongMetadata

__all__ = ["EmbedMetadataCommand"]


@dataclass
class EmbedMetadataCommand:
    path: Path
    metadata: SongMetadata
