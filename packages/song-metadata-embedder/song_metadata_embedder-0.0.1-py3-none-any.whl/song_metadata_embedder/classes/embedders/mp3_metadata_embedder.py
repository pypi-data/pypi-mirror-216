from pathlib import Path
import re
from typing import cast

import requests
from mutagen.mp3 import MP3, EasyMP3
from mutagen.id3 import ID3
from mutagen.id3._frames import APIC, COMM, WOAS, USLT, SYLT
from mutagen.id3._specs import Encoding

from song_metadata_embedder.classes import SongMetadata, TagPreset
from .abstract_metadata_embedder import AbstractMetadataEmbedder

LRC_REGEX = re.compile(r"(\[\d{2}:\d{2}.\d{2,3}\])")

__all__ = ["Mp3MetadataEmbedder"]


class Mp3MetadataEmbedder(AbstractMetadataEmbedder[MP3]):
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
            albumart="APIC",
            encodedby="encodedby",
            copyright="copyright",
            tempo="tempo",
            lyrics="lyrics",
            explicit="explicit",
            woas="woas",
        )

    def _load_file(self, path: Path) -> MP3:
        self._path = str(path.resolve())
        return EasyMP3(self._path)

    def _embed_specific(self, audio_file: MP3, metadata: SongMetadata) -> MP3:
        audio_file[self.tag_preset.tracknumber] = [
            f"{str(metadata.track_number)}/{str(metadata.track_count)}"
        ]

        audio_file[self.tag_preset.discnumber] = [
            f"{str(metadata.disc_number)}/{str(metadata.disc_count)}"
        ]

        audio_file.save(v2_version=3)
        audio_file = MP3(self._path)

        tags = cast(ID3, audio_file.tags)
        tags.add(WOAS(encoding=3, url=metadata.url))

        if metadata.download_url:
            tags.add(COMM(encoding=3, text=metadata.download_url))

        if metadata.popularity:
            tags.add(
                COMM(
                    encoding=3,
                    lang="eng",
                    text="Spotify Popularity: " + str(metadata.popularity),
                )
            )

        return audio_file

    def _embed_cover(self, audio_file: MP3, metadata: SongMetadata) -> MP3:
        if metadata.cover_url is None:
            return audio_file

        tags = cast(ID3, audio_file.tags)

        try:
            cover_data = requests.get(metadata.cover_url, timeout=10).content
        except Exception:
            return audio_file

        tags[self.tag_preset.albumart] = APIC(
            encoding=3,
            mime="image/jpeg",
            type=3,
            desc="Cover",
            data=cover_data,
        )

        return audio_file

    def _embed_lyrics(self, audio_file: MP3, metadata: SongMetadata) -> MP3:
        if metadata.lyrics is None:
            return audio_file

        tags = cast(ID3, audio_file.tags)

        # Check if the lyrics are in lrc format
        # using regex on the first 5 lines
        lrc_lines = metadata.lyrics.splitlines()[:5]
        lrc_lines = [line for line in lrc_lines if line and LRC_REGEX.match(line)]

        if len(lrc_lines) == 0:
            # Lyrics are not in lrc format
            # Embed them normally
            tags.add(USLT(encoding=Encoding.UTF8, text=metadata.lyrics))
        else:
            # Lyrics are in lrc format
            # Embed them as SYLT id3 tag
            lrc_data = []

            for line in metadata.lyrics.splitlines():
                time_tag = line.split("]", 1)[0] + "]"
                text = line.replace(time_tag, "")

                time_tag = time_tag.replace("[", "")
                time_tag = time_tag.replace("]", "")
                time_tag = time_tag.replace(".", ":")
                time_tag_vals = time_tag.split(":")
                if len(time_tag_vals) != 3 or any(
                    not isinstance(tag, int) for tag in time_tag_vals
                ):
                    continue

                minute, sec, millisecond = time_tag_vals
                time = self._to_ms(min=int(minute), sec=int(sec), ms=int(millisecond))
                lrc_data.append((text, time))

            tags.add(USLT(encoding=3, text=metadata.lyrics))
            tags.add(SYLT(encoding=Encoding.UTF8, text=lrc_data, format=2, type=1))

        return audio_file

    def _to_ms(self, hour: int = 0, min: int = 0, sec: int = 0, ms: int = 0) -> float:
        return 3600 * 1000 * hour + min * 60 * 1000 + sec * 1000 + ms

    def _save(self, audio_file: MP3):
        return audio_file.save(v2_version=3)
