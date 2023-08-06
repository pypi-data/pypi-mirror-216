from taipan_di import PipelineLink

from song_metadata_embedder.classes import EmbedMetadataCommand

__all__ = ["BaseMetadataEmbedder"]


BaseMetadataEmbedder = PipelineLink[EmbedMetadataCommand, None]
