from __future__ import annotations

from agents.base import Agent, Identifier
from models.modality import Lyrics
from models.protocol import FromLyricsResponse


class LyricsFinder(Identifier[str, FromLyricsResponse]):
  endpoint_name = 'from_lyrics'

  @classmethod
  def _preprocess_inputs(cls, data: str | Lyrics) -> str:
    return data.lyrics if isinstance(data, Lyrics) else data


class LyricsAnalyzer(Agent[str, list[FromLyricsResponse]]):
  finder_cls = LyricsFinder
