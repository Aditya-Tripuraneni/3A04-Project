from __future__ import annotations

import pydantic, typing as t


class Artist(pydantic.BaseModel):
  name: str
  gender: str


class Lyrics(pydantic.BaseModel):
  lyrics: str
  language: str


class Song(pydantic.BaseModel):
  name: str
  artist: Artist
  lyrics: Lyrics


class Album(pydantic.BaseModel):
  name: str
  genre: str
  year: str
  mood: str
  songs: list[Song]
  featured_artists: t.Optional[list[Artist]] = None


class Description(pydantic.BaseModel):
  song: Song
  artist: Artist
  album: Album
  region: str


class Audio(pydantic.BaseModel):
  audio_file: str
  song: t.Optional[Song] = None
