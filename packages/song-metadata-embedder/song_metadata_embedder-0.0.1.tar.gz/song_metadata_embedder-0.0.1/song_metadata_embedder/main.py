from pathlib import Path
from taipan_di import ServiceCollection

from song_metadata_embedder.classes import SongMetadata, EmbedMetadataCommand
from song_metadata_embedder.di import add_song_metadata_embedder
from song_metadata_embedder.interfaces import BaseMetadataEmbedder

__all__ = ["SongMetadataEmbedder"]


class SongMetadataEmbedder:
    def __init__(self) -> None:
        services = ServiceCollection()
        add_song_metadata_embedder(services)
        provider = services.build()

        self._embedder = provider.resolve(BaseMetadataEmbedder)

    def embed(self, path: Path, metadata: SongMetadata) -> None:
        command = EmbedMetadataCommand(path, metadata)
        self._embedder.exec(command)
