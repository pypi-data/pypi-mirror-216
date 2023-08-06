from taipan_di import ServiceCollection

from song_metadata_embedder.classes import (
    FlacMetadataEmbedder,
    M4AMetadataEmbedder,
    Mp3MetadataEmbedder,
    OggMetadataEmbedder,
    OpusMetadataEmbedder,
    FlacMetadataHandler,
    M4AMetadataHandler,
    Mp3MetadataHandler,
    OggMetadataHandler,
    OpusMetadataHandler,
)
from song_metadata_embedder.interfaces import BaseMetadataEmbedder

__all__ = ["add_song_metadata_embedder"]


def add_song_metadata_embedder(services: ServiceCollection) -> ServiceCollection:
    services.register(FlacMetadataEmbedder).as_factory().with_self()
    services.register(M4AMetadataEmbedder).as_factory().with_self()
    services.register(Mp3MetadataEmbedder).as_factory().with_self()
    services.register(OggMetadataEmbedder).as_factory().with_self()
    services.register(OpusMetadataEmbedder).as_factory().with_self()

    services.register_pipeline(BaseMetadataEmbedder).add(FlacMetadataHandler).add(
        Mp3MetadataHandler
    ).add(M4AMetadataHandler).add(OggMetadataHandler).add(OpusMetadataHandler).as_factory()

    return services
