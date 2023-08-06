from typing import Any

from song_metadata_embedder.classes.embedders import (
    M4AMetadataEmbedder,
    AbstractMetadataEmbedder,
)
from song_metadata_embedder.classes.handlers import AbstractMetadataHandler

__all__ = ["M4AMetadataHandler"]


class M4AMetadataHandler(AbstractMetadataHandler):
    def __init__(self, embedder: M4AMetadataEmbedder) -> None:
        self._embedder = embedder

    @property
    def encoding(self) -> str:
        return "m4a"

    @property
    def embedder(self) -> AbstractMetadataEmbedder[Any]:
        return self._embedder
