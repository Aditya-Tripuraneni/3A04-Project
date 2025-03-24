from __future__ import annotations

import typing as t
import pydantic

from models.modality import Song, Album


class FromFileResponse(pydantic.BaseModel):
  name: str
  artist: str
  confidence: float


class FromDescriptionResponse(pydantic.BaseModel):
  name: str
  artist: str
  confidence: float


class FromLyricsResponse(pydantic.BaseModel):
  name: str
  artist: str
  confidence: float
