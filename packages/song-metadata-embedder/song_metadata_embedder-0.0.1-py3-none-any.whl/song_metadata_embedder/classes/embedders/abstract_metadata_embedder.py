import abc
from pathlib import Path
from typing import Generic, TypeVar

from mutagen._file import FileType

from song_metadata_embedder.classes import SongMetadata, TagPreset, EmbedMetadataCommand
from song_metadata_embedder.errors import SongMetadataFileError

__all__ = ["AbstractMetadataEmbedder"]

T = TypeVar("T", bound=FileType)


class AbstractMetadataEmbedder(Generic[T], metaclass=abc.ABCMeta):
    @property
    @abc.abstractmethod
    def tag_preset(self) -> TagPreset:
        raise NotImplementedError

    def embed(self, request: EmbedMetadataCommand) -> None:
        try:
            audio_file = self._load_file(request.path)
        except Exception as ex:
            raise SongMetadataFileError(ex) from ex

        audio_file = self._embed_metadata(audio_file, request.metadata)
        audio_file = self._embed_specific(audio_file, request.metadata)
        audio_file = self._embed_cover(audio_file, request.metadata)
        audio_file = self._embed_lyrics(audio_file, request.metadata)

        self._save(audio_file)

    @abc.abstractmethod
    def _load_file(self, path: Path) -> T:
        raise NotImplementedError

    def _embed_metadata(self, audio_file: T, metadata: SongMetadata) -> T:
        audio_file[self.tag_preset.artist] = metadata.artists
        audio_file[self.tag_preset.albumartist] = [
            metadata.album_artist if metadata.album_artist else metadata.artist
        ]
        audio_file[self.tag_preset.title] = [metadata.title]
        audio_file[self.tag_preset.date] = [metadata.date]
        audio_file[self.tag_preset.encodedby] = [metadata.publisher]

        if metadata.album_name:
            audio_file[self.tag_preset.album] = [metadata.album_name]
        if metadata.genres:
            audio_file[self.tag_preset.genre] = metadata.genres[0].title()
        if metadata.copyright_text:
            audio_file[self.tag_preset.copyright] = [metadata.copyright_text]

        return audio_file

    @abc.abstractmethod
    def _embed_specific(self, audio_file: T, metadata: SongMetadata) -> T:
        raise NotImplementedError

    @abc.abstractmethod
    def _embed_cover(self, audio_file: T, metadata: SongMetadata) -> T:
        raise NotImplementedError

    @abc.abstractmethod
    def _embed_lyrics(self, audio_file: T, metadata: SongMetadata) -> T:
        raise NotImplementedError

    def _save(self, audio_file: T):
        audio_file.save()
