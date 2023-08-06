from typing import Any

from song_metadata_embedder.classes.embedders import (
    OggMetadataEmbedder,
    AbstractMetadataEmbedder,
)
from song_metadata_embedder.classes.handlers import AbstractMetadataHandler

__all__ = ["OggMetadataHandler"]


class OggMetadataHandler(AbstractMetadataHandler):
    def __init__(self, embedder: OggMetadataEmbedder) -> None:
        self._embedder = embedder

    @property
    def encoding(self) -> str:
        return "ogg"

    @property
    def embedder(self) -> AbstractMetadataEmbedder[Any]:
        return self._embedder
