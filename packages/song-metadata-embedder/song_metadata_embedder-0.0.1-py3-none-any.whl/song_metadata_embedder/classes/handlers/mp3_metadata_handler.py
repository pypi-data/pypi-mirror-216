from typing import Any

from song_metadata_embedder.classes.embedders import (
    Mp3MetadataEmbedder,
    AbstractMetadataEmbedder,
)
from song_metadata_embedder.classes.handlers import AbstractMetadataHandler

__all__ = ["Mp3MetadataHandler"]


class Mp3MetadataHandler(AbstractMetadataHandler):
    def __init__(self, embedder: Mp3MetadataEmbedder) -> None:
        self._embedder = embedder

    @property
    def encoding(self) -> str:
        return "mp3"

    @property
    def embedder(self) -> AbstractMetadataEmbedder[Any]:
        return self._embedder
