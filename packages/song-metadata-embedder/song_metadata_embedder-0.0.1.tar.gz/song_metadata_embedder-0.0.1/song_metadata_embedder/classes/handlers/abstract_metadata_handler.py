import abc
from typing import Any, Callable


from song_metadata_embedder.classes import EmbedMetadataCommand
from song_metadata_embedder.classes.embedders import AbstractMetadataEmbedder
from song_metadata_embedder.interfaces import BaseMetadataEmbedder

__all__ = ["AbstractMetadataHandler"]


class AbstractMetadataHandler(BaseMetadataEmbedder, metaclass=abc.ABCMeta):
    @property
    @abc.abstractmethod
    def encoding(self) -> str:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def embedder(self) -> AbstractMetadataEmbedder[Any]:
        raise NotImplementedError

    def _handle(
        self, request: EmbedMetadataCommand, next: Callable[[EmbedMetadataCommand], None]
    ) -> None:
        encoding = request.path.suffix[1:]

        if encoding != self.encoding:
            return next(request)

        self.embedder.embed(request)
