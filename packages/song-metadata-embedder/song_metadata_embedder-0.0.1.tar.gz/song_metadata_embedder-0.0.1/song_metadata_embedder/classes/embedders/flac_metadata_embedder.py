from pathlib import Path

import requests
from mutagen.flac import Picture, FLAC

from song_metadata_embedder.classes import SongMetadata, TagPreset
from .abstract_metadata_embedder import AbstractMetadataEmbedder

__all__ = ["FlacMetadataEmbedder"]


class FlacMetadataEmbedder(AbstractMetadataEmbedder[FLAC]):
    @property
    def tag_preset(self) -> TagPreset:
        return TagPreset(
            album="album",
            artist="artist",
            date="date",
            title="title",
            year="year",
            comment="comment",
            group="group",
            writer="writer",
            genre="genre",
            tracknumber="tracknumber",
            albumartist="albumartist",
            discnumber="discnumber",
            cpil="cpil",
            albumart="albumart",
            encodedby="encodedby",
            copyright="copyright",
            tempo="tempo",
            lyrics="lyrics",
            explicit="explicit",
            woas="woas",
        )

    def _load_file(self, path: Path) -> FLAC:
        return FLAC(str(path.resolve()))

    def _embed_specific(self, audio_file: FLAC, metadata: SongMetadata) -> FLAC:
        if metadata.download_url:
            audio_file[self.tag_preset.comment] = [metadata.download_url]

        zfilled_disc_number = str(metadata.disc_number).zfill(len(str(metadata.disc_count)))
        zfilled_track_number = str(metadata.track_number).zfill(
            len(str(metadata.track_count))
        )

        audio_file[self.tag_preset.tracknumber] = [zfilled_track_number]
        audio_file[self.tag_preset.discnumber] = [zfilled_disc_number]

        if metadata.url:
            audio_file[self.tag_preset.woas] = [metadata.url]

        return audio_file

    def _embed_cover(self, audio_file: FLAC, metadata: SongMetadata) -> FLAC:
        if metadata.cover_url is None:
            return audio_file

        try:
            cover_data = requests.get(metadata.cover_url, timeout=10).content
        except Exception:
            return audio_file

        picture = Picture()
        picture.type = 3
        picture.desc = "Cover"
        picture.mime = "image/jpeg"
        picture.data = cover_data

        audio_file.add_picture(picture)

        return audio_file

    def _embed_lyrics(self, audio_file: FLAC, metadata: SongMetadata) -> FLAC:
        if metadata.lyrics is None:
            return audio_file

        audio_file[self.tag_preset.lyrics] = [metadata.lyrics]
        return audio_file
