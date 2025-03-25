from audio import Audio
from controller import Controller
from description import Description
from lyrics import Lyrics
from models import LyricsRequest, DescriptionRequest, AudioRequest, SongPredictionResponse
from fastapi import FastAPI 
import logging

app = FastAPI()


@app.post("/analyze_song")
async def analyze_song(
    lyrics_request: LyricsRequest = None,
    description_request: DescriptionRequest = None
):
    """
    Analyzes the provided song data (lyrics, audio, description) and returns the predicted song,
    artist, and confidence score.
    """

    controller = Controller()

    if lyrics_request:
        lyrics = Lyrics(lyrics_request.lyrics)
        # analyze the lyrics data
        controller.analyze_data(lyrics)

    # if audio_request:
    #     audio = Audio(audio_request.audio_file)
    #     # analyze the audio data
    #     controller.analyze_data(audio)
        
    if description_request:
        description = Description(**description_request.model_dump())
        # analyze the description data
        controller.analyze_data(description)
    

    final_song = controller.finalize_solution()

    final_song_data = final_song.get_song_data()

    # return the predicted song, artist, and confidence score dynmically unpacked
    return SongPredictionResponse(**final_song_data)

