# Song Metadata Embedder

**Embed metadata into your music files, whatever the type**

## Features

- Automatic type detection based on the file extension
    - Currently supported : MP3, M4A, FLAC, OGG (Vorbis), OPUS
- Detection of badly formatted files
- Easy to use, straightforward interface
- Possible to use via DI integration

## Installation

### Pip

```
pip install song-metadata-embedder
```

### Poetry

[Poetry](https://python-poetry.org/) is a Python dependency management and packaging tool. I actually use it for this project.

```
poetry add song-metadata-embedder
```

## Usage

There are 2 ways to use this library : using the SongMetadataEmbedder object or via the DI.

### Using SongMetadataEmbedder

The library exposes the SongMetadataEmbedder class. This class has 1 method : `embed`.

This method detects the type of the file you want to modify and sets the metadata accordingly.

**Example :**

```python
from pathlib import Path
from song_metadata_embedder import SongMetadataEmbedder, SongMetadata

embedder = SongMetadataEmbedder()
path = Path("path/to/file.mp3")
metadata = SongMetadata(...)

embedder.embed(path, metadata)
```

### Using DI

The library also exposes a `BaseMetadataEmbedder` interface and a `add_song_metadata_embedder` function for [Taipan-DI](https://github.com/Billuc/Taipan-DI).

In this function, the embedders are registered as a Pipeline. All you need to do is to resolve the pipeline and execute it.

**Example :**

```python
from song_metadata_embedder import BaseMetadataEmbedder, add_song_metadata_embedder, SongMetadata, EmbedMetadataCommand
from taipan_di import DependencyCollection

services = DependencyCollection()
add_song_metadata_embedder(services)
provider = services.build()

embedder = provider.resolve(BaseMetadataEmbedder)
path = Path("path/to/file.mp3")
metadata = SongMetadata(...)
command = EmbedMetadataCommand(path, metadata)

embedder.exec(command)
```

## Inspirations

This library is partially based on spotDL's [spotify-downloader](https://github.com/spotDL/spotify-downloader).
