from __future__ import annotations

from agents.base import Agent, Identifier
from models.modality import Description
from models.protocol import FromDescriptionResponse


class DescriptionFinder(Identifier[str, FromDescriptionResponse]):
  endpoint_name = 'from_text'

  @classmethod
  def _preprocess_inputs(cls, data: str | Description) -> str:
    return (
      f'Looking for a {data.album.genre} song by {data.artist.name} from the album {data.album.name} released in {data.album.year} region {data.region}.'
      if isinstance(data, Description)
      else data
    )


class DescriptionAnalyzer(Agent[str, list[FromDescriptionResponse]]):
  finder_cls = DescriptionFinder
