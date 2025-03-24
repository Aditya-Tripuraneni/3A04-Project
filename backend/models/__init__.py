# Import and re-export protocol models
from .modality import Artist, Lyrics, Song, Album, Description, Audio
from .protocol import FromFileResponse, FromDescriptionResponse, FromLyricsResponse

__all__ = [
  'Album',
  'Artist',
  'Audio',
  'Description',
  'FromDescriptionResponse',
  'FromFileResponse',
  'FromLyricsResponse',
  'Lyrics',
  'Song',
]
