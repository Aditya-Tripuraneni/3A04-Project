from pydantic import BaseModel

class LyricsRequest(BaseModel):
    lyrics: str

class AudioRequest(BaseModel):
    audio_file:str

class DescriptionRequest(BaseModel):
    artist: str
    genre: str
    year: str
    albumName: str
    mood: str
    genderOfArtist: str
    language: str
    region: str
    featuredArtist: str


class SongPredictionResponse(BaseModel):
    song_name: str = "Unknown Song"
    song_author: str = "Unknown Artist"
    confidence_score: float = 0.0