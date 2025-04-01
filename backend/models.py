from typing import List
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

class PredictedSong(BaseModel):
    song_name: str
    song_author: str
    confidence_score: float

class SongModel(BaseModel):
    song_name: str
    song_author: str 


class SongPredictionResponse(BaseModel):
    predicted_song: PredictedSong # main song predicted by the systen
    recommended_songs: List[SongModel] # list of songs recommended by the system



class AnalyzeRequest(BaseModel):
    lyrics_request: LyricsRequest | None = None
    audio_request: AudioRequest | None = None
    description_request: DescriptionRequest | None = None


class LogTransactionRequest(BaseModel):
    songName: str
    userGuess: str
    songIdentified: str
    accuracyScore: float
    recommendedArtists: List[str]
    timestamp: str