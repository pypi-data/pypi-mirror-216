from typing import Any

from song_metadata_embedder.classes.embedders import (
    OpusMetadataEmbedder,
    AbstractMetadataEmbedder,
)
from song_metadata_embedder.classes.handlers import AbstractMetadataHandler

__all__ = ["OpusMetadataEmbedder"]


class OpusMetadataHandler(AbstractMetadataHandler):
    def __init__(self, embedder: OpusMetadataEmbedder) -> None:
        self._embedder = embedder

    @property
    def encoding(self) -> str:
        return "opus"

    @property
    def embedder(self) -> AbstractMetadataEmbedder[Any]:
        return self._embedder
